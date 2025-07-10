import cv2
import time
import math as m
import mediapipe as mp

# ========== Helper Functions ==========

def findDistance(x1, y1, x2, y2):
    return m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def findAngle(x1, y1, x2, y2):
    try:
        theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
        return int(180 / m.pi) * theta
    except:
        return 0

def sendWarning(x=None):
    pass

# ========== Main Function ==========

def generate_desk_frames():
    good_frames = 0
    bad_frames = 0
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Colors
    green = (127, 255, 0)
    red = (50, 50, 255)
    light_green = (127, 233, 100)
    yellow = (0, 255, 255)
    pink = (255, 0, 255)

    # MediaPipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_pose_landmark = mp_pose.PoseLandmark
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    fps = 30

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        h, w = image.shape[:2]
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = pose.process(image_rgb)
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        lm = result.pose_landmarks
        if not lm:
            continue

        # Draw landmarks on every frame
        mp_drawing.draw_landmarks(image, lm, mp_pose.POSE_CONNECTIONS)

        # Get coordinates
        l_shldr = lm.landmark[mp_pose_landmark.LEFT_SHOULDER]
        r_shldr = lm.landmark[mp_pose_landmark.RIGHT_SHOULDER]
        l_ear = lm.landmark[mp_pose_landmark.LEFT_EAR]
        l_hip = lm.landmark[mp_pose_landmark.LEFT_HIP]

        l_shldr_x, l_shldr_y = int(l_shldr.x * w), int(l_shldr.y * h)
        r_shldr_x, r_shldr_y = int(r_shldr.x * w), int(r_shldr.y * h)
        l_ear_x, l_ear_y = int(l_ear.x * w), int(l_ear.y * h)
        l_hip_x, l_hip_y = int(l_hip.x * w), int(l_hip.y * h)

        # Alignment check
        offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)
        align_color = green if offset < 100 else red
        align_text = f"{int(offset)} {'Aligned' if offset < 100 else 'Not Aligned'}"
        cv2.putText(image, align_text, (w - 250, 30), font, 0.8, align_color, 2)

        # Angles
        neck_incl = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
        torso_incl = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)
        angle_text = f'Neck: {int(neck_incl)}  Torso: {int(torso_incl)}'

        is_good = neck_incl < 30 and torso_incl < 10
        color = light_green if is_good else red
        good_frames = good_frames + 1 if is_good else 0
        bad_frames = bad_frames + 1 if not is_good else 0

        # Draw annotations
        cv2.putText(image, angle_text, (10, 30), font, 0.9, color, 2)
        cv2.putText(image, str(int(neck_incl)), (l_shldr_x + 10, l_shldr_y), font, 0.9, color, 2)
        cv2.putText(image, str(int(torso_incl)), (l_hip_x + 10, l_hip_y), font, 0.9, color, 2)

        for pt in [(l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), (l_shldr_x, l_shldr_y - 100),
                   (r_shldr_x, r_shldr_y), (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100)]:
            cv2.circle(image, pt, 7, yellow if pt != (r_shldr_x, r_shldr_y) else pink, -1)

        cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), color, 4)
        cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), color, 4)
        cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), color, 4)
        cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), color, 4)

        good_time = round((1 / fps) * good_frames, 1)
        bad_time = round((1 / fps) * bad_frames, 1)
        time_msg = f"{'Good' if is_good else 'Bad'} Posture Time : {good_time if is_good else bad_time}s"
        cv2.putText(image, time_msg, (10, h - 20), font, 0.9, color, 2)

        if bad_time > 180:
            sendWarning()

        # Encode frame and yield for MJPEG
        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()
