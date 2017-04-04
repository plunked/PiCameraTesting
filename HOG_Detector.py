import time
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file (optional)")
args = vars(ap.parse_args())

# Use attached webcam if no arguments. Use video file otherwise. 

if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

#initialise HOG
HOG = cv2.HOGDescriptor()
HOG.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
time.sleep(0.1)

while True:

    (grabbed, frame) = camera.read()
    if args.get("video") and not grabbed:
        break
    
    hogRects, w = HOG.detectMultiScale(frame, winStride=(8, 8), padding=(32, 32), scale=1.05)
    frameClone = frame.copy()

    for (fX, fY, fW, fH) in hogRects:
        cv2.rectangle(frameClone, (fX, fY), (fX+fW, fY+fH), (0, 255, 0), 2)
    
    cv2.imshow('feed', frameClone)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break