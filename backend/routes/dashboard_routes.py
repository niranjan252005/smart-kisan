from flask import Blueprint, jsonify
import os, requests
from openai import OpenAI

dashboard_bp = Blueprint("dashboard", __name__)

# OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# WEATHER
@dashboard_bp.route("/api/weather")
def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=19.0760&longitude=72.8777&current_weather=true"
    data = requests.get(url).json()

    cw = data.get("current_weather", {})

    return jsonify({
        "temp": cw.get("temperature", "--"),
        "humidity": 50,
        "wind": cw.get("windspeed", "--")
    })


# SOIL
@dashboard_bp.route("/api/soil")
def get_soil():
    return jsonify({
        "N": 60,
        "P": 45,
        "K": 70,
        "moisture": 12,
        "temp": 24
    })


# ----------------------------
#  AI-BASED GOV SCHEMES
# ----------------------------
@dashboard_bp.route("/api/schemes")
def ai_schemes():
    prompt = """
    Give 6 Indian government schemes useful for farmers.
    Each item must have:
    - title
    - short description (20-30 words)
    - official link (if known, else "#")
    Return ONLY JSON list.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.choices[0].message.content
        import json
        return jsonify(json.loads(text))

    except Exception as e:
        print("AI SCHEMES ERROR:", e)
        return jsonify([])


# ----------------------------
#  AI-BASED LIVE MARKET PRICES
# ----------------------------
@dashboard_bp.route("/api/market")
def ai_market():
    prompt = """
    Generate today's modal market prices for 10 crops in India.
    Include fields:
    - crop
    - price (₹ per quintal)
    - state
    - market
    Return ONLY JSON list.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.choices[0].message.content
        import json
        return jsonify(json.loads(text))

    except Exception as e:
        print("AI MARKET ERROR:", e)
        return jsonify([])



# CROP DATASET
@dashboard_bp.route("/api/crops")
def get_crops():
    url = "https://raw.githubusercontent.com/rajkumardusad/Indian-Crop-Dataset/master/crop_recommendation.json"
    try:
        data = requests.get(url, timeout=5).json()
    except:
        return jsonify(["Wheat", "Rice", "Maize", "Cotton", "Sugarcane"])

    crops = list({item["label"] for item in data})
    return jsonify(crops[:6])


# NOTIFICATIONS
@dashboard_bp.route("/api/notifications")
def notifications():
    return jsonify([
        "Rain alert in your region",
        "New mandi prices generated",
        "2 new government schemes for farmers"
    ])

@dashboard_bp.route("/api/search")
def search_query():
    from flask import request
    q = request.args.get("q", "").lower()

    responses = {
        "wheat": "Wheat grows best in well-drained loamy soil.",
        "rice": "Rice requires standing water and high humidity.",
        "fertilizer": "Use NPK 10:26:26 for initial growth."
    }

    for key in responses:
        if key in q:
            return jsonify({"result": responses[key]})
    
    return jsonify({"result": "No data found"})
