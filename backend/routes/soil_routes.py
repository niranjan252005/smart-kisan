from flask import Blueprint, request

soil_bp = Blueprint("soil", __name__)

@soil_bp.route("/check", methods=["POST"])
def soil_check():
    soil_type = request.json.get("soil_type")

    mock = {
        "black soil": "Best for cotton & sugarcane",
        "red soil": "Suitable for millets & pulses",
        "clay soil": "Good for rice & wheat"
    }

    return {"result": mock.get(soil_type.lower(), "Unknown soil type")}
