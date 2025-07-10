import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import Video from './Components/Video';
import WebCam from './Components/WebCam';
import Live from './Live';
import {BrowserRouter,Routes,Route} from 'react-router-dom'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
         <Route path="/" element={<App/>} />
        <Route path="/Video" element={<Video/>} />
        <Route path="/WebCam" element={<Live/>} />
        <Route path="/WebCamSquat" element={<WebCam flag = '0'/>} />
        <Route path="/WebCamBack" element={<WebCam flag = '1'/>} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

