import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [image, setImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [prediction, setPrediction] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    setImage(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const handleSubmit = async () => {
    if (!image) {
      alert("Please upload an image first.");
      return;
    }

    const formData = new FormData();
    formData.append('file', image);

    try {
      const response = await axios.post('https://us-central1-flower-classification-427503.cloudfunctions.net/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      const { data } = response;
      setPrediction(`Predicted response is ${data.class} with confidence ${data.confidence}`);
    } catch (error) {
      console.error("There was an error making the request", error);
      setPrediction("There was an error making the request");
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <input type="file" onChange={handleImageUpload} />
      {previewUrl && <img src={previewUrl} alt="Preview" style={{ width: '300px', marginTop: '20px' }} />}
      <div>
        <button onClick={handleSubmit} style={{ marginTop: '20px' }}>Upload and Predict</button>
      </div>
      {prediction && <div style={{ marginTop: '20px' }}>{prediction}</div>}
    </div>
  );
}

export default App;
