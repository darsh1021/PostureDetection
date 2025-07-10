
import './App.css';
import { useNavigate } from "react-router-dom";


function App() {
 
       function video()
      {
       navigate("/Video");
      }

       function webCam()
      {
       navigate("/WebCam");
      }

  const navigate = useNavigate();

  return (<>
<div className="page-container">
  <h1 className="main-heading">🧍‍♂️ Posture Check</h1>

  <div className="button-group">
    <button className="custom-button" onClick={video}>📤 Upload Video</button>
    <button className="custom-button" onClick={webCam}>📷 Allow Webcam</button>
  </div>

  <div className="info-section">
    <div className="info-box upload-box">
      <h2>📤 Upload Video</h2>
      <p>
        Upload a side-view video of yourself performing 3 full squats. Ensure your
        full body is clearly visible and well-lit for accurate posture detection.
      </p>
    </div>

    <div className="info-box webcam-box">
      <h2>📷 Allow Webcam</h2>
      <p>
        Enable your webcam for live squat tracking. Stand sideways and ensure the
        camera captures your full body from head to feet in a bright area.
      </p>
    </div>
  </div>
</div>

    </>);
}

export default App;
