import cv2
import numpy as np
import dlib

#BGR color
BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)

cap = cv2.VideoCapture(0)
count = 0

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def midpoint(p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def length(p1, p2):
    return int(np.sqrt((p1[0] - p1[0])**2+(p2[1] - p1[1])**2))

while True:
    _ , frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)

        leftEye_L = (landmarks.part(36).x, landmarks.part(36).y)
        leftEye_R = (landmarks.part(39).x, landmarks.part(39).y)
        rightEye_L = (landmarks.part(42).x, landmarks.part(36).y)
        rightEye_R = (landmarks.part(45).x, landmarks.part(39).y)
        # cv2.circle(frame, (x,y), 3, RED, 2)
        H_left_eye = cv2.line(frame, leftEye_L, leftEye_R, GREEN, 2)
        H_right_eye = cv2.line(frame, rightEye_L, rightEye_R, GREEN, 2)

        leftEye_T = midpoint(landmarks.part(37), landmarks.part(38))
        leftEye_B = midpoint(landmarks.part(41), landmarks.part(40))
        rightEye_T = midpoint(landmarks.part(43), landmarks.part(44))
        rightEye_B = midpoint(landmarks.part(47), landmarks.part(46))

        V_left_eye = cv2.line(frame, leftEye_T, leftEye_B, GREEN, 2)
        V_right_eye = cv2.line(frame, rightEye_T, rightEye_B, GREEN, 2)

        # print(length(leftEye_T, leftEye_B))
        # print(length(rightEye_T, rightEye_B))

        blink_threshold = 7

        if length(leftEye_T, leftEye_B) < blink_threshold and \
            length(rightEye_T, rightEye_B) < blink_threshold:
            count+=1
            left_len = length(leftEye_T, leftEye_B)
            right_len = length(rightEye_T, rightEye_B)
            print("Blinked", count, left_len, right_len)

        # cv2.circle(frame, (x,y), 3, RED, 2)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()