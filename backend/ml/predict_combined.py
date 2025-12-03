# backend/ml/predict_combined.py
import os, json
import numpy as np
from .preprocess import load_image_from_path, to_batch

# Lazy-loaded model storage
_models = {
    "disease": None,   # TensorFlow Keras model
    "croprec": None,   # sklearn/xgboost joblib
    "soil": None,
}

MODEL_DIR = os.path.join(os.getcwd(), "backend", "ml_models")

def _load_disease_model():
    global _models
    if _models["disease"] is None:
        try:
            import tensorflow as tf
            model_path = os.path.join(MODEL_DIR, "disease_model")
            if os.path.exists(model_path):
                _models["disease"] = tf.keras.models.load_model(model_path)
            else:
                _models["disease"] = None
        except Exception as e:
            print("disease model load error:", e)
            _models["disease"] = None

def _load_croprec_model():
    global _models
    if _models["croprec"] is None:
        try:
            import joblib
            p = os.path.join(MODEL_DIR, "croprec.joblib")
            if os.path.exists(p):
                _models["croprec"] = joblib.load(p)
            else:
                _models["croprec"] = None
        except Exception as e:
            print("croprec load error:", e)
            _models["croprec"] = None

def _load_soil_model():
    global _models
    if _models["soil"] is None:
        try:
            import joblib
            p = os.path.join(MODEL_DIR, "soil_model.joblib")
            if os.path.exists(p):
                _models["soil"] = joblib.load(p)
            else:
                _models["soil"] = None
        except Exception as e:
            print("soil model load error:", e)
            _models["soil"] = None

def predict_all_from_path(img_path):
    """
    Returns a combined result dict
    """
    # Ensure models loaded lazily
    _load_disease_model()
    _load_croprec_model()
    _load_soil_model()

    result = {}

    # 1) Disease inference (TF model)
    if _models["disease"] is not None:
        img = load_image_from_path(img_path, target_size=(224,224))
        batch = to_batch(img)
        preds = _models["disease"].predict(batch)
        # handle both softmax vector or dict output
        if isinstance(preds, np.ndarray):
            # assume single output softmax
            idx = int(np.argmax(preds[0]))
            score = float(np.max(preds[0]))
            # label map file (optional)
            label_file = os.path.join(MODEL_DIR, "disease_labels.json")
            if os.path.exists(label_file):
                with open(label_file,'r') as f: labels = json.load(f)
                label = labels[idx] if idx < len(labels) else str(idx)
            else:
                label = str(idx)
            result["disease"] = label
            result["disease_conf"] = score
        else:
            result["disease"] = str(preds)
            result["disease_conf"] = None
    else:
        # fallback dummy
        result["disease"] = "Healthy"
        result["disease_conf"] = 0.9

    # 2) Crop Recommendation (sklearn)
    if _models["croprec"] is not None:
        # We need features for crop recommendation (NPK, pH, weather). If you only have an image,
        # you can have a separate soil inference or use placeholders. Here I show a placeholder.
        features = _extract_features_for_croprec(img_path)
        try:
            pred = _models["croprec"].predict([features])[0]
            proba = None
            if hasattr(_models["croprec"], "predict_proba"):
                proba = float(max(_models["croprec"].predict_proba([features])[0]))
            result["crop"] = str(pred)
            result["crop_conf"] = proba
        except Exception as e:
            result["crop"] = "Wheat"
            result["crop_conf"] = 0.8
    else:
        result["crop"] = "Wheat"
        result["crop_conf"] = 0.8

    # 3) Soil health (if model present)
    if _models["soil"] is not None:
        features = _extract_features_for_soil(img_path)
        try:
            s = _models["soil"].predict([features])[0]
            result["soil"] = str(s)
        except Exception as e:
            result["soil"] = "Good"
    else:
        result["soil"] = "Good"

    return result

def _extract_features_for_croprec(img_path):
    # Implement your own feature extraction:
    # e.g., use average color channels, simple heuristics, or integrate a small model
    from PIL import Image
    import numpy as np
    im = Image.open(img_path).convert("RGB").resize((100,100))
    arr = np.array(im)/255.0
    mean_rgb = arr.mean(axis=(0,1)).tolist()
    # placeholder features: mean R,G,B
    return mean_rgb[:3]

def _extract_features_for_soil(img_path):
    # placeholder: re-use same features as croprec
    return _extract_features_for_croprec(img_path)
