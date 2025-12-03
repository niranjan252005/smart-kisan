from flask import Blueprint, request
from backend.utils.ml_utils import analyze_crop_image, recommend_best_crop

crop_bp = Blueprint("crop", __name__)

@crop_bp.route("/analyze", methods=["POST"])
def analyze_crop():
    image = request.files["image"]
    path = "uploaded.jpg"
    image.save(path)

    result = analyze_crop_image(path)
    return result


@crop_bp.route("/recommend", methods=["POST"])
def recommend_crop():
    data = request.json
    location = data.get("location")
    soil = data.get("soil")
    weather = data.get("weather")

    result = recommend_best_crop(location, soil, weather)
    return result
