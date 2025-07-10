from flask import Flask, request, jsonify
from flask_cors import CORS
import os 
from posture_analysis import process_video
from flask import Flask, Response
from flask_cors import CORS
from webcam_squat import generate_squat_frames
from webcam_desk import generate_desk_frames

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "✅ Flask server running!"

@app.route('/upload', methods=['POST'])
def upload_and_process():
    if 'video' not in request.files:
        return jsonify({'message': 'No video file provided'}), 400

    video = request.files['video']
    filepath = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(filepath)

    result = process_video(filepath)
    return jsonify({'message': result})

@app.route('/squat_feed')
def squat_feed():
    return Response(generate_squat_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/desk_feed')
def desk_feed():
    return Response(generate_desk_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
