import cv2
import numpy as np
import dlib

#BGR color
BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)
font = cv2.FONT_HERSHEY_SIMPLEX

CAM_WIDTH = 1280
CAM_HEIGHT = 720

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

detector = dlib.get_frontal_face_detector()

#check in area
def in_area(x,y):
    x_center = CAM_WIDTH/2
    y_center = CAM_HEIGHT/2

    x_diff = x-x_center
    y_diff = y-y_center

    dist = np.sqrt(x_diff**2 + y_diff**2)
    angle = np.arctan2(y_diff, x_diff)
    print("dist:{}, angle:{}".format(dist, angle))

while True:
    _ , frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        xc = int((x+x1)/2)
        yc = int((y+y1)/2)
        in_area(xc, yc)
        cv2.rectangle(frame, (x,y), (x1,y1), GREEN, 2)
        v_line = cv2.line(frame, (xc,0), (xc,CAM_HEIGHT), GREEN, 2)
        h_line = cv2.line(frame, (0,yc), (CAM_WIDTH,yc), GREEN, 2)
        cv2.putText(frame, 'x:{}, y:{}'.format(xc,yc),
                   (xc+20, yc-20), font, 1, GREEN, 2, cv2.LINE_AA)

    # if xc > 1280/2:
    #     print("left")
    # else:
    #     print("right")
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()