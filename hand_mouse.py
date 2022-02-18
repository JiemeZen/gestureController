import mediapipe as mp
import cv2
import numpy as np
import uuid
import os

from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller
import time

mouse = Controller()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

CAM_WIDTH = 1280
CAM_HEIGHT = 720
SCREEN_WIDTH = 2560
SCREEN_HEIGHT = 1440

count = 0

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

def midpoint(p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def distance(x1, y1, x2, y2):
    dist = np.sqrt((x2-x1)**2+(y2-y1)**2)
    return dist

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 
    while cap.isOpened():
        ret, frame = cap.read()
        
        # BGR 2 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Flip on horizontal
        image = cv2.flip(image, 1)
        
        # Set flag
        image.flags.writeable = False
        
        # Detections
        results = hands.process(image)
        
        # Set flag to true
        image.flags.writeable = True
        
        # RGB 2 BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Detections
        # print(results)
        
        # Rendering results
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                         )
        
            pos_x = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
            pos_y = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
            screenPos_x = int(pos_x*SCREEN_WIDTH)
            screenPos_y = int(pos_y*SCREEN_HEIGHT)
            # print("x:{:.2f}, y:{:.2f}".format(pos_x*CAM_WIDTH, pos_y*CAM_HEIGHT))
            
            mouse.position = (screenPos_x, screenPos_y)

            index_x = int(100*(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x))
            index_y = int(100*(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y))
            thumb_x = int(100*(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_TIP].x))
            thumb_y = int(100*(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_TIP].y))

            print(distance(index_x, index_y, thumb_x, thumb_y))
            if distance(index_x, index_y, thumb_x, thumb_y) < 5:
                count+=1
            
            if count > 5:
                print("clicked")
                mouse.press(Button.left)
                mouse.release(Button.left)
                count = 0

        # mp_drawing.draw_landmarks(image, results.multi_hand_landmarks.INDEX_FINGER_MCP, 
        #                             results.HAND_CONNECTIONS)        
        cv2.imshow('Hand Tracking', image)

        key = cv2.waitKey(1)
        if key == 27:
            break

cap.release()
cv2.destroyAllWindows()