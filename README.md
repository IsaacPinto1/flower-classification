# Project README

## Getting Started

### How to Run the Website

To run this website locally, follow these steps:

1. Navigate to the Project Folder: `cd path/to/your/project`
2. Install Dependencies: `npm install`
3. Start the Development Server: `npm run start`
4. Open your web browser and navigate to: `http://localhost:3000`

The website should now be running locally on your machine.

### Requirements:
- Node.js

---

## Model Training and Deployment

### Model Training

- The model was trained using the TensorFlow flowers dataset available at [this link](https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz).
- The training process is documented in the 'training.ipynb' file located under the 'training' folder.
- To minimize the impact of overfitting, data augmentation techniques, such as random rotation, zoom, and contrast, as well as dropout layers were used during the training process.
- TensorFlow version used: 2.13.0.

### Model Export

- After training, the model was exported in the SavedModel format using the following code: `model.save("../models/flowerspredict")`.

### Local Testing

- For local testing, use 'localtest.py', which includes code to upload a local image path for prediction.

### Deployment on Google Cloud

1. **Setup:**
   - Download and install the Google Cloud SDK following the instructions [here](https://cloud.google.com/sdk/docs/install).
   - Create a Google Cloud project at [console.cloud.google.com](https://console.cloud.google.com).

2. **Model Upload:**
   - Create a bucket in Google Cloud Storage and upload your tarball (`flowerpredict.tar.gz`) to `/models/`.
   - Note the bucket name used and the path to the model

3. **Deploying Google Cloud Function:**
   - Update the constants in your `main.py` file:
     ```python
     BUCKET_NAME = # Your bucket name
     MODEL_TARBALL = # Path to your model, e.g /models/flowerpredict.tar.gz
     MODEL_DIR = "/tmp/flowerpredict"
     ```
   - Deploy the function using the Google Cloud SDK:
     ```
     sudo ~/google-cloud-sdk/bin/gcloud functions deploy predict --runtime python38 --trigger-http --memory 1GB --project [YOUR_PROJECT_ID]
     ```
     Replace `[YOUR_PROJECT_ID]` with your actual Google Cloud project ID.

4. **Integration:**
   - Obtain the trigger URL generated after deploying the function.
   - Integrate this URL into your front-end application to make HTTP requests for predictions.

---
