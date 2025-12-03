import joblib
import numpy as np

MODEL = joblib.load("ml_models/croprec.joblib")

with open("ml_models/crop_labels.txt") as f:
    LABELS = [line.strip() for line in f.readlines()]

def recommend_crop(N, P, K, temp, humidity, ph, rainfall):
    X = np.array([[N, P, K, temp, humidity, ph, rainfall]])
    pred_class = MODEL.predict(X)[0]
    return LABELS[pred_class]
