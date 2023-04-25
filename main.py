import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
print(screen_w, screen_h)
SCALE_FACTOR = 2
RIGHT_CLICK = False
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    
    landmark_points = output.multi_face_landmarks
    # print(landmark_points)
    # print(np.shape(landmark_points))
    
    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark
        # print(landmarks)
        # print(np.shape(landmarks))
        right_up = landmarks[385]
        right_down = landmarks[252]
        x = int(right_up.x * frame_w)
        y = int(right_up.y * frame_h)
        cv2.circle(frame, (x, y), 3, (0, 255, 0))
        x = int(right_down.x * frame_w)
        y = int(right_down.y * frame_h)
        cv2.circle(frame, (x, y), 3, (0, 255, 0))
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            # cv2.circle(frame, (x, y), 3, (0, 255, 0))
            # cv2.putText(frame, str(id), (x, y),
            # cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
            if id == 1:
                
                screen_x = int(screen_w/2)+ (landmark.x-0.5)*screen_w*SCALE_FACTOR
                screen_y = int(screen_h/2)+ (landmark.y-0.5)*screen_h*SCALE_FACTOR
                
                

                pyautogui.moveTo(screen_x, screen_y)
        if (abs(right_up.y - right_down.y) < 0.018) and RIGHT_CLICK:
            pyautogui.rightClick()
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        if (left[0].y - left[1].y) < 0.014:
            pyautogui.leftClick()
            # pyautogui.sleep(1)
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)