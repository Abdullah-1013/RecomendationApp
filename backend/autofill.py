from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import uuid

app = Flask(__name__)

def autofill_air_conditioner(name):
    # Example scraping logic (replace with real scraping)
    return {
        "name": name,
        "price_pkr": 45000,
        "brand": "LG",
        "image_url": "",
        "power_input_cooling_min_kw": 1.2,
        "power_input_cooling_max_kw": 2.0,
        "hours_per_day": 8,
        "lifetime_years": 10,
        "refrigerant_type": "R410A",
        "air_flow_volume_m3h": 500,
        "type": "Split",
        "capacity_ton": 1.5,
        "energy_rating_stars": 5,
        "indoor_noise_db": 45,
        "notes": "",
        "created_at": datetime.utcnow().isoformat()
    }

def autofill_car(name):
    return {
        "name": name,
        "fuel_type": "Petrol",
        "displacement_cc": 1500,
        "engine_power_kw": 100,
        "torque_nm": 140,
        "transmission_type": "Manual",
        "fuel_tank_capacity_l": 45,
        "seating_capacity": 5,
        "production_emissions": 120,
        "use_phase_emissions": 3000,
        "lifetime_years": 10,
        "recycling_rate": 0.85,
        "image_url": "",
        "created_at": datetime.utcnow().isoformat(),
        "price": 2500000
    }

def autofill_bike(name):
    return {
        "name": name,
        "engine_capacity_cc": 125,
        "mileage_kmpl": 55.0,
        "fuel_tank_liters": 8.5,
        "dry_weight_kg": 100,
        "image_url": "",
        "brand": "Honda",
        "bike_type": "Standard",
        "price_pkr": 150000
    }

def autofill_record(name):
    return {
        "network_technology": "4G",
        "launch_announced": "2025",
        "launch_status": "Available",
        "body_dimensions": "150x70x8 mm",
        "body_weight": "150g",
        "sim": "Dual SIM",
        "display_type": "LCD",
        "display_size": "6.1",
        "display_resolution": "1080x2400",
        "platform_os": "Android",
        "platform_cpu": "Octa-core",
        "platform_gpu": "Mali-G57",
        "memory_card_slot": "Yes",
        "memory_internal": "128GB",
        "main_camera_single": "48MP",
        "selfie_camera": "16MP",
        "battery_type": "Li-Po 4000 mAh",
        "price": "35000",
        "image_url": "",
        "name": name
    }

@app.route("/autofill/<table>", methods=["GET"])
def autofill(table):
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Missing name"}), 400

    try:
        if table == "air_conditioners":
            data = autofill_air_conditioner(name)
        elif table == "cars":
            data = autofill_car(name)
        elif table == "bikes":
            data = autofill_bike(name)
        elif table == "records":
            data = autofill_record(name)
        else:
            return jsonify({"error": "Invalid table"}), 400
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
