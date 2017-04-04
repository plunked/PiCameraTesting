from facedetector import FaceDetector
import imutils
from picamera import PiCamera
from picamera.array import PiRGBArray
import argparse
import time
import cv2

#constructing argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

#initializing PiCamera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = (32)
camera.vflip = True
rawCapture = PiRGBArray(camera, size=(640, 480))

#constructing the detector
HOG = cv2.HOGDescriptor()
HOG.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
time.sleep(0.1)

#frame rawCapture
for frames in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frames.array
    frame = imutils.resize(frame, width=300)

    hogRects, w = HOG.detectMultiScale(frame, winStride=(8, 8), padding=(32, 32), scale=1.05)
    frameClone = frame.copy()

    for (fX, fY, fW, fH) in hogRects:
        cv2.rectangle(frameClone, (fX, fY), (fX+fW, fY+fH), (0, 255, 0), 2)

    cv2.imshow("feed", frameClone)
    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

