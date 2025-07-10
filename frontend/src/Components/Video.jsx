import './video.css';
import React, { useState } from 'react';

function Video() {
  const [loading, setLoading] = useState(false);

  function handleUpload(event) {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('video', file);

    setLoading(true);

    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    })
      .then(res => res.json())
      .then(data => {
        alert(data.message); 
        setLoading(false);  
      })
      .catch(err => {
        console.error(err);
        alert("❌ Upload failed.");
        setLoading(false);
      });
  }

  return (
    <div className="uploader-container">
      <h2 className="uploader-title">🎥 Upload Video</h2>
      
      <input
        type="file"
        accept="video/*"
        className="uploader-input"
        onChange={handleUpload}
      />

      {loading && <p className="loading-text">⏳ Processing video... Please wait.</p>}
    </div>
  );
}

export default Video;
