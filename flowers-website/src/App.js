import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; // Import your CSS file for styling

function App() {
  const [image, setImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loadingText, setLoadingText] = useState('Loading'); // Initial loading text
  const [isLoading, setIsLoading] = useState(false); // State for loading indicator
  const [fileName, setFileName] = useState(''); // State to store uploaded file name

  useEffect(() => {
    if (isLoading) {
      const interval = setInterval(() => {
        setLoadingText(prevText => {
          switch (prevText) {
            case 'Loading':
              return 'Loading.';
            case 'Loading.':
              return 'Loading..';
            case 'Loading..':
              return 'Loading...';
            case 'Loading...':
              return 'Loading';
            default:
              return 'Loading';
          }
        });
      }, 500); // Adjust the interval as needed for the animation speed

      return () => clearInterval(interval);
    }
  }, [isLoading]);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (!file) {
      return;
    }
    setPrediction("")
    setImage(file);
    setFileName(file.name); // Set the file name
    setPreviewUrl(URL.createObjectURL(file)); // Set preview URL
  };

  const handleSubmit = async () => {
    if (!image) {
      alert("Please upload an image first.");
      return;
    }

    setIsLoading(true); // Start loading animation

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
    } finally {
      setIsLoading(false); // Stop loading animation
    }
  };

  return (
    <div className="app-container">
      {/* Styled file input */}
      <label className="upload-label">
        <input type="file" onChange={handleImageUpload} className="upload-input" />
        Upload Image
      </label>
      <br/>
      {fileName && <div className="file-name">File: {fileName}</div>} {/* Display file name */}
      {previewUrl && <img src={previewUrl} alt="Preview" className="preview-image" />}
      <div>
        <button onClick={handleSubmit} className="submit-button">Predict</button>
      </div>
      {isLoading && <div className="loading-text">{loadingText}</div>} {/* Animated loading text */}
      {prediction && !isLoading && <div className="prediction">{prediction}</div>} {/* Display prediction if not loading */}
    </div>
  );
}

export default App;
