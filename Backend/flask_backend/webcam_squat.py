import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))
    return angle

def generate_squat_frames():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            # Get points
            ear = [lm[mp_pose.PoseLandmark.LEFT_EAR.value].x,
                   lm[mp_pose.PoseLandmark.LEFT_EAR.value].y]
            shoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            hip = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            # ✅ Back angle: Ear - Shoulder - Hip
            back_angle = calculate_angle(ear, shoulder, hip)

            # ❗Warn if torso leans too far
            if back_angle < 150:
                cv2.putText(frame, "⚠️ Torso Lean < 150°", (30, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # ❗Warn if knee goes past toe
            if knee[0] > ankle[0]:
                cv2.putText(frame, "⚠️ Knee beyond toe", (30, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # ✅ Knee bend angle
            knee_angle = calculate_angle(hip, knee, ankle)

            if knee_angle < 80:
                status = "✔️ Full Squat"
                color = (0, 255, 0)
            elif knee_angle < 120:
                status = "⚠️ Half Squat"
                color = (0, 255, 255)
            else:
                status = "❌ Not a Squat"
                color = (0, 0, 255)

            # 📝 Overlay info
            cv2.putText(frame, f"Back: {int(back_angle)}°", (30, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f"Knee: {int(knee_angle)}°", (30, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(frame, status, (30, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(frame, "🔄 Squat Posture Detection", (30, 460),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 255, 100), 2)

            # Draw pose
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Stream frame
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()
