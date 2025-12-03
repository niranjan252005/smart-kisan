# backend/routes/ml_routes.py
from flask import Blueprint, request, jsonify
import os, time, base64
from werkzeug.utils import secure_filename
from backend.ml.predict_combined import predict_all_from_path
from backend.ml.preprocess import load_image_from_path

ml_bp = Blueprint("ml_bp", __name__)

UPLOAD_DIR = os.path.join(os.getcwd(), "backend", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@ml_bp.route("/analyze", methods=["POST"])
def analyze():
    # accept multipart/form-data file or JSON base64 {image: "data:..."}
    if request.content_type and request.content_type.startswith("application/json"):
        payload = request.get_json()
        dataurl = payload.get("image")
        if not dataurl:
            return jsonify({"success": False, "message": "No image"}), 400
        header, b64 = dataurl.split(",",1)
        import base64
        b = base64.b64decode(b64)
        fname = f"img_{int(time.time()*1000)}.jpg"
        path = os.path.join(UPLOAD_DIR, fname)
        with open(path, "wb") as f:
            f.write(b)
    else:
        f = request.files.get("image") or request.files.get("file")
        if not f:
            return jsonify({"success": False, "message": "No file."}), 400
        fname = secure_filename(f.filename)
        path = os.path.join(UPLOAD_DIR, f"{int(time.time()*1000)}_{fname}")
        f.save(path)

    # run combined prediction
    try:
        res = predict_all_from_path(path)
        return jsonify({"success": True, "result": res})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
