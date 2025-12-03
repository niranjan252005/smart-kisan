import numpy as np
from PIL import Image
import joblib

MODEL_PATH = "models/disease_model.joblib"
model = joblib.load(MODEL_PATH)

def predict_disease(image_path):
    img = Image.open(image_path).convert("RGB").resize((64, 64))
    img = np.array(img).flatten().reshape(1, -1)
    return model.predict(img)[0]
