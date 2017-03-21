from facedetector import FaceDetector
import imutils
from picamera import PiCamera
from picamera.array import PiRGBArray
import argparse
import time
import cv2

#constructing argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required=True, help="path to the face cascade")
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

#initializing PiCamera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = (32)
rawCapture = PiRGBArray(camera, size=(640, 480))

#constructing the detector
fd = FaceDetector(args["face"])
time.sleep(0.1)

#frame rawCapture
for frames in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frames.array
    frame = imutils.resize(frame, width=300)

    #detecting the faces and then cloning so as to draw

    faceRects = fd.detect(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (30, 30))
    frameClone = frame.copy()

    for (fX, fY, fW, fH) in faceRects:
		cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH), (0, 255, 0), 2)

	# show our detected faces, then clear the frame in
	# preparation for the next frame
	cv2.imshow("Face", frameClone)
	rawCapture.truncate(0)

	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

