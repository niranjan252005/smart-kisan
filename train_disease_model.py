import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

DATASET_PATH = "smart_kisan_starter/dataset"

def load_images(path):
    X = []
    y = []

    if not os.path.exists(path):
        print("❌ DATASET PATH NOT FOUND:", path)
        return [], []

    main_labels = os.listdir(path)

    for label in main_labels:
        label_folder = os.path.join(path, label)

        if not os.path.isdir(label_folder):
            continue

        for sub_item in os.listdir(label_folder):
            sub_folder = os.path.join(label_folder, sub_item)

            if not os.path.isdir(sub_folder):
                continue

            for img_file in os.listdir(sub_folder):
                img_path = os.path.join(sub_folder, img_file)

                try:
                    img = Image.open(img_path).convert("RGB").resize((64, 64))
                    X.append(np.array(img).flatten())
                    y.append(label)
                except Exception as e:
                    print("⚠️ Error loading:", img_path, "|", e)

    return np.array(X), np.array(y)


# ---------------------------
# RUN TRAINING
# ---------------------------
if __name__ == "__main__":
    print("📥 Loading images...")
    X, y = load_images(DATASET_PATH)

    print("📸 Total images loaded:", len(X))
    print("🏷 Labels found:", set(y))

    if len(X) == 0:
        print("❌ No images loaded — CHECK DATASET PATH:", DATASET_PATH)
        print("Your dataset folder must look like:")
        print("dataset/")
        print("   ├── healthy/")
        print("   │      ├── tomato_healthy/")
        print("   │      ├── pepper_bell_healthy/")
        print("   │      └── potato_healthy/")
        print("   ├── diseased/")
        print("   │      ├── tomato_diseased/")
        print("   │      ├── pepper_bell_diseased/")
        print("   │      └── potato_diseased/")
        exit()

    print("📊 Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    print("🤖 Training model...")
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    print("🔍 Testing...")
    y_pred = model.predict(X_test)

    print("🎯 Accuracy:", accuracy_score(y_test, y_pred))

    joblib.dump(model, "disease_model.joblib")
    print("✅ Model saved as disease_model.joblib")
