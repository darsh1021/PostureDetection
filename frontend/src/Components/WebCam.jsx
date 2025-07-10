import React from 'react';
import "./webCam.css";

function WebCam(props) {

   let flag = props.flag ;
  return (
    <div >
      <h2>🔴 Live Webcam Feed</h2>

      {flag === '0' ? <img
        src="http://localhost:5000/squat_feed"
        alt="Allow Video "
        style={{
          width: '600px',
          borderRadius: '10px',
          boxShadow: '0 5px 20px rgba(0,0,0,0.3)'
        }}
      />:
      <img
        src="http://localhost:5000/desk_feed"
        alt="Allow Video "
        style={{
          width: '600px',
          borderRadius: '10px',
          boxShadow: '0 5px 20px rgba(0,0,0,0.3)'
        }}
      />}
      
    </div>
  );
}

export default WebCam;
