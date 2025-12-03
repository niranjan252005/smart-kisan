import numpy as np
import tensorflow as tf
from PIL import Image

# Load model once
interpreter = tf.lite.Interpreter(model_path="ml_models/crop_disease_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load labels
with open("ml_models/disease_labels.txt") as f:
    LABELS = [line.strip() for line in f.readlines()]

def predict_disease(image_path):
    img = Image.open(image_path).resize((224, 224))
    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = np.argmax(output)

    return LABELS[predicted_class]
