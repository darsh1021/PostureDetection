========================================================     Posture Detection        ===========================================================================================
A real-time posture detection web app using Flask (Python) and React (JavaScript). 
It uses Mediapipe and OpenCV to detect squat and desk posture from a webcam feed and provides visual and audio feedback.


========================================================    Tech Stack Used           ============================================================================================ 
##Frontend (React):
- React.js
- HTML, CSS, JavaScript

##Bakend (Flask)
- Python 3.8+
- Flask
- Flask-CORS
- OpenCV
- Mediapipe

========================================================    Set Up Instructions       ============================================================================================
##Requirements
python --version
npm --version


##Frontend
Path: frontend/
cd frontend
npm install
npm start


##Backend
Path: Backend/flask_backend/
cd Backend/flask_backend

python -m venv venv
venv\Scripts\activate        # On Windows

pip install -r requirements.txt
python app.py

=========================================================   Links  ==========================================================================================================
Link to deployed app  : https://posture-detection-psi.vercel.app/
**Frontend is Deployed 
**Backend is not deployed since Render not supporting MEDIAPIPE 

Link to demo video : 


