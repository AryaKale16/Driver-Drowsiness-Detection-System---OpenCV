# Importing OpenCV Library for basic image processing functions
import cv2
# Numpy for array related functions
import numpy as np
# Dlib for deep learning based Modules and face landmark detection
import dlib
# face_utils for basic operations of conversion
from imutils import face_utils
import pygame

pygame.mixer.init()
pygame.mixer.music.load('C:/Users/hp/PycharmProjects/pythonProject/venv/beep.mp3')

# Initializing the camera and taking the instance
cap = cv2.VideoCapture(0)

# Initializing the face detector and landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("C:/Users/hp/PycharmProjects/pythonProject/venv/shape_predictor_68_face_landmarks.dat")

# status marking for current state
sleep = 0
drowsy = 0
active = 0
status = ""
color = (0, 0, 0)


def compute(ptA, ptB):
    dist = np.linalg.norm(ptA - ptB)
    return dist

#Euclidean Eye Aspect Ratio
def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)

    # Checking if it is blinked
    if (ratio > 0.25):
        return 2
    elif (ratio > 0.21 and ratio <= 0.25):
        return 1
    else:
        return 0


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fra = cv2.rectangle(frame, (0, 0), (230, 70), (0, 0, 0), 10, None, None)
    faces = detector(gray)
    # detected face in faces array
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        face_copy: object = frame.copy()
        cv2.rectangle(face_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        # The numbers are actually the landmarks which will show eye
        left_blink = blinked(landmarks[36], landmarks[37],
                             landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43],
                              landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        # Now judge what to do for the eye blinks
        if (left_blink == 0 or right_blink == 0):
            sleep += 1
            drowsy = 0
            active = 0
            if (sleep > 6):
                pygame.mixer.music.play(-1)
                status = "SLEEPING         "#7
                color = (255, 0, 0)


        elif (left_blink == 1 or right_blink == 1):
            sleep = 0
            active = 0
            drowsy += 1
            if (drowsy > 6):
                pygame.mixer.music.stop()
                status = "DROWSY!!          "#8
                color = (0, 0, 255)

        else:
            drowsy = 0
            sleep = 0
            active += 1
            if (active > 6):
                pygame.mixer.music.stop()
                status = " ACTIVE            "#8
                color = (0, 200, 0)
        stat = "Facelandmarks"
        cv2.putText(frame, status, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, color, 3)
        cv2.putText(face_copy, stat, (10, 50), cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 2)

        for n in range(0, 68):
            (x, y) = landmarks[n]
            cv2.circle(face_copy, (x, y), 1, (255, 255, 255), -1)

    hor = np.hstack((frame,face_copy))
    cv2.imshow("Result",hor)
    # cv2.imshow("Drowsiness Status", frame)
    # cv2.imshow("Face Landmarks", face_copy)
    key = cv2.waitKey(1)
    if key == 27:
        break
