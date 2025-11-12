# main.py
from flask import Flask, jsonify
from supabase import create_client
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import pickle
import os
import threading
import time

# Supabase config
SUPABASE_URL = "https://ohqowvsqxtunqcadjlng.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9ocW93dnNxeHR1bnFjYWRqbG5nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE0NTk3MjYsImV4cCI6MjA3NzAzNTcyNn0.PT9LbmDEz-_8nvgAHhFRGUMo2X15y-UZfB5_Oqc_adQ"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

MODEL_FILE = "knn_model.pkl"
SCALER_FILE = "scaler.pkl"
USER_SUMMARY_FILE = "user_summary.pkl"

# ------------------ Data Fetching ------------------ #
def fetch_data():
    try:
        users = supabase.table("users").select("*").execute().data
        products = supabase.table("products").select("*").execute().data
        history = supabase.table("purchase_history").select("*").execute().data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    users_df = pd.DataFrame(users)
    products_df = pd.DataFrame(products)
    history_df = pd.DataFrame(history)

    # Ensure numeric and correct types
    if not products_df.empty:
        products_df["price"] = pd.to_numeric(products_df["price"], errors='coerce').fillna(0)
        products_df["sustainability"] = products_df["sustainability"].apply(
            lambda x: 1 if str(x).lower() in ["true","1","sustainable"] else 0
        )

    if not history_df.empty:
        history_df["price_paid"] = pd.to_numeric(history_df["price_paid"], errors='coerce').fillna(0)

    return users_df, products_df, history_df

# ------------------ Model Training ------------------ #
def train_and_save_model():
    users_df, products_df, history_df = fetch_data()
    if history_df.empty or products_df.empty:
        print("⚠️ Train failed: No data")
        return None, None, None

    # Create user-product pivot table
    merged = history_df.merge(products_df, left_on="product_id", right_on="id", how="left")
    merged["sustainability"] = merged["sustainability"].astype(int)
    merged["price_paid"] = merged["price_paid"].astype(float)

    pivot = merged.pivot_table(index="user_id", columns="product_id", values="price_paid", fill_value=0)
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(pivot)

    knn = NearestNeighbors(n_neighbors=5, metric="cosine")
    knn.fit(scaled)

    # Save model
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(knn, f)
    with open(SCALER_FILE, "wb") as f:
        pickle.dump(scaler, f)
    with open(USER_SUMMARY_FILE, "wb") as f:
        pickle.dump(pivot, f)

    print("✅ Auto retrain successful")
    return knn, scaler, pivot

def load_model():
    if all(os.path.exists(f) for f in [MODEL_FILE, SCALER_FILE, USER_SUMMARY_FILE]):
        try:
            with open(MODEL_FILE, "rb") as f:
                knn = pickle.load(f)
            with open(SCALER_FILE, "rb") as f:
                scaler = pickle.load(f)
            with open(USER_SUMMARY_FILE, "rb") as f:
                user_summary = pickle.load(f)
            return knn, scaler, user_summary
        except Exception as e:
            print(f"⚠️ Load model failed: {e}")
            return train_and_save_model()
    else:
        return train_and_save_model()

# ------------------ Recommendation ------------------ #
def recommend_for_user(user_id, n_recommend=5):
    users_df, products_df, history_df = fetch_data()
    knn, scaler, pivot = load_model()

    if products_df.empty or knn is None:
        print("⚠️ Recommendation error: No data or model")
        return []

    # Ensure numeric columns
    products_df["price"] = pd.to_numeric(products_df["price"], errors='coerce').fillna(0)
    products_df["sustainability"] = products_df["sustainability"].apply(
        lambda x: 1 if str(x).lower() in ["true","1","sustainable"] else 0
    )
    history_df["price_paid"] = pd.to_numeric(history_df["price_paid"], errors='coerce').fillna(0)

    user_history = history_df[history_df["user_id"] == user_id]

    # CASE 1: New user
    if user_history.empty:
        print("🟡 New user — showing mixed recommendations")
        users_with_history = history_df["user_id"].unique()
        purchased_ids = history_df[history_df["user_id"].isin(users_with_history)]["product_id"].unique()
        available_products = products_df[products_df["id"].isin(purchased_ids)]

        sustainable = available_products[available_products["sustainability"] == 1]
        non_sustainable = available_products[available_products["sustainability"] == 0]

        sustainable_sample = sustainable.sample(min(3, len(sustainable))) if len(sustainable) > 0 else pd.DataFrame()
        non_sustainable_sample = non_sustainable.sample(min(3, len(non_sustainable))) if len(non_sustainable) > 0 else pd.DataFrame()

        mixed = pd.concat([sustainable_sample, non_sustainable_sample])
        if mixed.empty:
            mixed = products_df.sample(min(n_recommend, len(products_df)))
        else:
            mixed = mixed.sample(frac=1).head(n_recommend)

        return mixed.to_dict(orient="records")

    # CASE 2: Existing user
    last_purchase = user_history.merge(products_df, left_on="product_id", right_on="id", how="left")
    if last_purchase["sustainability"].sum() > 0:
        avg_price = last_purchase["price_paid"].mean()
        sustainable_products = products_df[
            (products_df["sustainability"] == 1) & 
            (products_df["price"] <= avg_price)
        ]
        recommendations = sustainable_products.sample(min(n_recommend, len(sustainable_products))) \
                          if len(sustainable_products) > 0 else products_df.sample(min(n_recommend, len(products_df)))
    else:
        # User bought only non-sustainable → recommend all sustainable
        sustainable_products = products_df[products_df["sustainability"] == 1]
        recommendations = sustainable_products.sample(min(n_recommend, len(sustainable_products))) \
                          if len(sustainable_products) > 0 else products_df.sample(min(n_recommend, len(products_df)))

    return recommendations.to_dict(orient="records")

# ------------------ Routes ------------------ #
@app.route("/")
def index():
    return "✅ Recommendation Server is Running!"

@app.route("/recommend/<user_id>")
def recommend_api(user_id):
    try:
        recs = recommend_for_user(user_id)
        return jsonify(recs)
    except Exception as e:
        print(f"⚠️ Recommendation error: {e}")
        return jsonify({"error": str(e)}), 500

# ------------------ Auto Retrain Thread ------------------ #
def auto_retrain(interval=3600):
    while True:
        try:
            train_and_save_model()
        except Exception as e:
            print(f"⚠️ Auto retrain error: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    threading.Thread(target=auto_retrain, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True)
