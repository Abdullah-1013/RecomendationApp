from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
from supabase import create_client, Client
import pickle
import threading
import time
import os
import math

# ---------------------------------------------------
# SUPABASE CONFIG
# ---------------------------------------------------
SUPABASE_URL = "https://yweqmaqruqnemntvpxel.supabase.co" 
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl3ZXFtYXFydXFuZW1udHZweGVsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA3OTQwOTgsImV4cCI6MjA0NjM3MDA5OH0.caT9BazwCZuil5X1d8zVWeBrZINRTPxQiyL4nxBHblA"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
CORS(app)

MODEL_FILE = "simple_model.pkl"


# ===================================================
# HELPER FUNCTIONS
# ===================================================

def cosine_similarity(list1, list2):
    dot = sum(a * b for a, b in zip(list1, list2))
    mag1 = math.sqrt(sum(a * a for a in list1))
    mag2 = math.sqrt(sum(a * a for a in list2))
    return dot / (mag1 * mag2) if mag1 and mag2 else 0


def fetch_data():
    """Fetch all required tables"""
    try:
        users = supabase.table("users").select("*").execute().data
        products = supabase.table("products").select("*").execute().data
        history = supabase.table("purchase_history").select("*").execute().data
        return users, products, history
    except Exception as e:
        print("Fetch Error:", e)
        return [], [], []


# ===================================================
# SECTION 1 — PRODUCT CHECK + INSERT
# ===================================================

@app.route("/check_by_name", methods=["GET"])
def check_by_name():
    table = request.args.get("table")
    name = request.args.get("name")

    result = supabase.table(table).select("*").eq("name", name).execute()
    if result.data:
        return jsonify({"exists": True, "data": result.data})
    return jsonify({"exists": False})


@app.route("/check_product", methods=["GET"])
def check_product():
    qr_id = request.args.get("qr_id")
    table = request.args.get("table")

    result = supabase.table(table).select("*").eq("id", qr_id).execute()
    if result.data:
        return jsonify({"exists": True, "data": result.data})
    return jsonify({"exists": False})


@app.route("/insert_product", methods=["POST"])
def insert_product():
    data = request.json
    table = data.get("table")
    product_data = data.get("data")

    product_data["uuid"] = str(uuid.uuid4())
    product_data["created_at"] = datetime.utcnow().isoformat()

    supabase.table(table).insert(product_data).execute()
    return jsonify({"message": "Product added successfully"})


# ===================================================
# SECTION 2 — RECOMMENDATION SYSTEM (PURE PYTHON)
# ===================================================

def train_and_save_model():
    users, products, history = fetch_data()

    if not products or not history:
        print("Not enough data to train model")
        return None

    # Create dictionary: { user_id: { product_id: price_paid } }
    user_matrix = {}

    for purchase in history:
        uid = purchase["user_id"]
        pid = purchase["product_id"]
        price = float(purchase.get("price_paid", 0))

        if uid not in user_matrix:
            user_matrix[uid] = {}
        user_matrix[uid][pid] = price

    pickle.dump(user_matrix, open(MODEL_FILE, "wb"))
    print("Model trained successfully")
    return user_matrix


def load_model():
    if os.path.exists(MODEL_FILE):
        return pickle.load(open(MODEL_FILE, "rb"))
    return train_and_save_model()


def recommend_for_user(user_id, n=5):
    users, products, history = fetch_data()
    matrix = load_model()

    if user_id not in matrix:
        # New user → return random products
        return products[:n]

    target_vector = matrix[user_id]

    similarities = []
    for other_user, product_vector in matrix.items():
        if other_user == user_id:
            continue
        common_products = sorted(set(target_vector) | set(product_vector))

        v1 = [target_vector.get(pid, 0) for pid in common_products]
        v2 = [product_vector.get(pid, 0) for pid in common_products]

        sim = cosine_similarity(v1, v2)
        similarities.append((other_user, sim))

    # sort by highest similarity
    similarities.sort(key=lambda x: x[1], reverse=True)

    if not similarities:
        return products[:n]

    best_user = similarities[0][0]
    purchased_by_best = matrix[best_user].keys()

    recommended = [p for p in products if p["id"] in purchased_by_best]
    return recommended[:n]


@app.route("/recommend/<user_id>")
def recommend_api(user_id):
    try:
        data = recommend_for_user(user_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})


# ===================================================
# AUTO RE-TRAIN (EVERY 1 HOUR)
# ===================================================
def auto_retrain(interval=3600):
    while True:
        train_and_save_model()
        time.sleep(interval)


@app.route("/")
def home():
    return "🔥 Backend Running (Products + Recommendations)"


if __name__ == "__main__":
    threading.Thread(target=auto_retrain, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True)
