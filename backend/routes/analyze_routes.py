import os
import joblib
from flask import Blueprint, request, jsonify
from PIL import Image
import numpy as np

analyze_bp = Blueprint("analyze_routes", __name__, url_prefix="/api")

# ---------------- LOAD MODEL SAFELY ----------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, "disease_model.joblib")

print("🔍 Looking for model at:", MODEL_PATH)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model not found at: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)
print("✔ ML Model Loaded Successfully:", MODEL_PATH)


# ---------------- PROCESS IMAGE ----------------
def preprocess_image(image):
    img = Image.open(image).convert("RGB")
    img = img.resize((64, 64))
    img = np.array(img).flatten().reshape(1, -1)
    return img


# ---------------- ROUTE ----------------
@analyze_bp.route("/predict", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    x = preprocess_image(file)
    prediction = model.predict(x)[0]

    return jsonify({
        "success": True,
        "prediction": str(prediction)
    })
