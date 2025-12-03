# backend/ml/preprocess.py
from PIL import Image
import numpy as np
import io

def load_image_from_path(path, target_size=(224,224)):
    im = Image.open(path).convert("RGB")
    im = im.resize(target_size)
    arr = np.array(im) / 255.0
    return arr

def load_image_from_bytes(b64bytes, target_size=(224,224)):
    # b64bytes = base64.b64decode(...) before calling or pass raw bytes
    im = Image.open(io.BytesIO(b64bytes)).convert("RGB")
    im = im.resize(target_size)
    arr = np.array(im) / 255.0
    return arr

def to_batch(x):
    import numpy as np
    return np.expand_dims(x, axis=0).astype('float32')
