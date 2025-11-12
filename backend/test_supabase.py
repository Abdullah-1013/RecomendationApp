from flask import Flask, jsonify
from supabase import create_client
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import pickle
import os

app = Flask(__name__)

# ---------------- SUPABASE CONFIG ----------------
SUPABASE_URL = "https://ohqowvsqxtunqcadjlng.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9ocW93dnNxeHR1bnFjYWRqbG5nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE0NTk3MjYsImV4cCI6MjA3NzAzNTcyNn0.PT9LbmDEz-_8nvgAHhFRGUMo2X15y-UZfB5_Oqc_adQ"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

MODEL_FILE = "knn_model.pkl"
SCALER_FILE = "scaler.pkl"
USER_SUMMARY_FILE = "user_summary.pkl"

# ---------------- HELPER FUNCTIONS ----------------
def fetch_data():
    users = supabase.table("users").select("*").execute().data
    products = supabase.table("products").select("*").execute().data
    history = supabase.table("purchase_history").select("*").execute().data

    users_df = pd.DataFrame(users)
    products_df = pd.DataFrame(products)
    history_df = pd.DataFrame(history)

    # Ensure price_paid exists
    if 'price_paid' not in history_df.columns:
        history_df['price_paid'] = np.nan

    return users_df, products_df, history_df

def train_and_save_model():
    users_df, products_df, history_df = fetch_data()

    # Merge user purchase info
    merged = history_df.merge(products_df, left_on='product_id', right_on='id', how='left')
    user_summary = merged.groupby('user_id').agg({
        'sustainability': 'mean',
        'price_paid': 'mean'
    }).fillna(0)

    X = user_summary[['sustainability', 'price_paid']].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    knn = NearestNeighbors(n_neighbors=3, metric='euclidean')
    knn.fit(X_scaled)

    # Save model, scaler, summary
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(knn, f)
    with open(SCALER_FILE, 'wb') as f:
        pickle.dump(scaler, f)
    with open(USER_SUMMARY_FILE, 'wb') as f:
        pickle.dump(user_summary, f)

    return knn, scaler, user_summary

def load_model():
    if os.path.exists(MODEL_FILE) and os.path.exists(SCALER_FILE) and os.path.exists(USER_SUMMARY_FILE):
        knn = pickle.load(open(MODEL_FILE, 'rb'))
        scaler = pickle.load(open(SCALER_FILE, 'rb'))
        user_summary = pickle.load(open(USER_SUMMARY_FILE, 'rb'))
        return knn, scaler, user_summary
    else:
        return train_and_save_model()

# ---------------- RECOMMENDATION FUNCTION ----------------
def recommend_for_user(user_id):
    users_df, products_df, history_df = fetch_data()
    knn, scaler, user_summary = load_model()

    # If user has no history, fallback to default recommendation
    if user_id not in user_summary.index:
        sustainable_products = products_df[products_df['sustainability'] == True]
        if len(sustainable_products) > 0:
            recs_df = sustainable_products.sample(n=min(5, len(sustainable_products)))
        else:
            recs_df = products_df.sample(n=min(5, len(products_df)))
        return recs_df.to_dict(orient='records')

    # Get user vector
    user_vector = user_summary.loc[user_id][['sustainability', 'price_paid']].values.reshape(1, -1)
    user_vector_scaled = scaler.transform(user_vector)

    # Find nearest neighbors
    distances, indices = knn.kneighbors(user_vector_scaled)
    neighbor_ids = user_summary.iloc[indices[0]].index.tolist()

    # Recommend sustainable products
    recs_df = products_df[products_df['sustainability'] == True]
    if len(recs_df) == 0:
        recs_df = products_df  # fallback
    recs_df = recs_df.sample(n=min(5, len(recs_df)))

    return recs_df.to_dict(orient='records')

# ---------------- API ROUTE ----------------
@app.route("/recommend/<user_id>")
def recommend_api(user_id):
    try:
        recs = recommend_for_user(user_id)
        return jsonify(recs)
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    try:
        train_and_save_model()
        print("✅ Initial training successful")
    except Exception as e:
        print("⚠️ Train failed:", e)

    app.run(host="0.0.0.0", port=5000, debug=True)
