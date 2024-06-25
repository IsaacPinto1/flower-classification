import tensorflow as tf
from PIL import Image
import numpy as np
import tarfile
import os

# Define the class names
class_names = ["daisy", "dandelion", "roses", "sunflowers", "tulips"]

# Path to the model tarball and extraction directory
tarball_path = "./models/flowerpredict.tar.gz"  # Update with your local path
model_dir = "flowerpredict"
IMG_HEIGHT, IMG_WIDTH = 180, 180

# Extract the tarball if not already extracted
def extract_tarball(tarball_path, extract_path):
    with tarfile.open(tarball_path, "r:gz") as tar:
        tar.extractall(path=extract_path)
    print(f"Extracted {tarball_path} to {extract_path}.")

extract_tarball(tarball_path, model_dir)

# Load the model
model = tf.keras.models.load_model(model_dir + "/flowerpredict")

# Function to preprocess and predict the class of the image
def predict(image_path):
    img = Image.open(image_path).convert("RGB").resize((IMG_HEIGHT, IMG_WIDTH))
    img_array = np.array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print("Predictions:", predictions)
    print("Softmax score:", score)

    predicted_class = class_names[np.argmax(score)]
    confidence = round(100 * np.max(score), 2)

    return {"class": predicted_class, "confidence": confidence}

# Test the model with a sample image
sample_image_path = "./training/datasets/flower_photos/roses/12240303_80d87f77a3_n.jpg"  # Update with your local image path
result = predict(sample_image_path)
print(result)