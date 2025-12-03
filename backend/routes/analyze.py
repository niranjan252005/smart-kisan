import os, joblib
from flask import Blueprint, request, jsonify
from PIL import Image
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

page_bp = Blueprint("analyze", __name__, url_prefix="/api")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, "disease_model.joblib")
model = joblib.load(MODEL_PATH)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

KB = {
    "healthy": {
        "reason": "The leaf is healthy. No disease patterns found.",
        "remedies": "No treatment required.",
        "pesticides": "None."
    },
    "leaf_blight": {
        "reason": "Leaf blight is caused by bacterial infection usually in humid climates.",
        "remedies": "Remove infected leaves, avoid overhead irrigation.",
        "pesticides": "Copper Oxychloride, Mancozeb."
    },
    "rust": {
        "reason": "Rust is caused by fungal spores spread by wind.",
        "remedies": "Improve airflow, prune infected areas.",
        "pesticides": "Hexaconazole, Propiconazole."
    }
}

def preprocess_image(file):
    img = Image.open(file).convert("RGB")
    img_small = img.resize((64, 64))
    x = np.array(img_small).flatten().reshape(1, -1)
    return img, x

def ai_explain_disease(disease_name):
    try:
        prompt = f"""
Provide a detailed 15–20 line explanation of the crop disease '{disease_name}'.
Include:
1. Causes
2. How it spreads
3. Early & advanced symptoms
4. Environmental risk factors
5. Impact on crop yield
6. Prevention methods
7. Field management tips
8. Best pesticides with dosages
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an agriculture expert."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("AI ERROR:", e)
        return None

@page_bp.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    img, x = preprocess_image(file)

    pred = model.predict(x)[0]
    confidence = round(model.predict_proba(x).max() * 100, 2)

    info = KB[pred]

    explanation = ai_explain_disease(pred)
    if not explanation:
        explanation = (
            f"{info['reason']}\n\n"
            f"Remedies:\n{info['remedies']}\n\n"
            f"Pesticides:\n{info['pesticides']}"
        )

    return jsonify({
        "disease": pred,
        "confidence": confidence,
        "severity": "medium",
        "health_score": 70,
        "reason": info["reason"],
        "remedies": info["remedies"],
        "pesticides": info["pesticides"],
        "explanation": explanation    # FIXED
    })
