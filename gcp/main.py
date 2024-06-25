from google.cloud import storage
import tensorflow as tf
from PIL import Image
import numpy as np
import tarfile
import os
from flask import Flask, request, jsonify

model = None
class_names = ["daisy", "dandelion", "roses", "sunflowers", "tulips"]

BUCKET_NAME = "flower-classification-isaac"
MODEL_TARBALL = "models/flowerpredict.tar.gz"
MODEL_DIR = "/tmp/flowerpredict"
IMG_HEIGHT, IMG_WIDTH = 180, 180

app = Flask(__name__)

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

def extract_tarball(tarball_path, extract_path):
    """Extracts a tarball to the specified path."""
    with tarfile.open(tarball_path, "r:gz") as tar:
        tar.extractall(path=extract_path)
    print(f"Extracted {tarball_path} to {extract_path}.")

@app.route('/predict', methods=['POST'])
def predict(request):
    global model
    if model is None:
        tarball_path = "/tmp/flowerpredict.tar.gz"
        download_blob(BUCKET_NAME, MODEL_TARBALL, tarball_path)
        extract_tarball(tarball_path, "/tmp")
        model = tf.keras.models.load_model(MODEL_DIR)

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    image = Image.open(file).convert("RGB").resize((IMG_HEIGHT, IMG_WIDTH))
    img_array = np.array(image)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    predicted_class = class_names[np.argmax(score)]
    confidence = round(100 * np.max(score), 2)

    response = jsonify({
        "class": predicted_class,
        "confidence": confidence
    })

    # Add CORS headers
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST")

    return response

if __name__ == '__main__':
    app.run(debug=True)


#sudo ~/google-cloud-sdk/bin/gcloud functions deploy predict --runtime python38 --trigger-http --memory 1GB --project flower-classification-427503
