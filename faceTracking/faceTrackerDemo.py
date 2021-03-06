from faceDetector import FaceDetector
import imutils
import argparse
import time
import cv2

#constructing argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required=True, help="path to the face cascade")
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

#initializing camera
camera = cv2.VideoCapture(1)

#constructing the detector
fd = FaceDetector(args["face"])
time.sleep(0.1)

#performing detection
while True:
    (grabbed, frame) = camera.read()
    if args.get("video") and not grabbed:
        break
    
    frame = imutils.resize(frame, width=300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #detecting the faces and then cloning so as to draw
    faceRects = fd.detect(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    frameClone = frame.copy()

    for (fX, fY, fW, fH) in faceRects:
        cv2.rectangle(frameClone, (fX, fY), (fX+fW, fY+fH), (0, 255, 0), 2)

    cv2.imshow("Face", frameClone)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
        