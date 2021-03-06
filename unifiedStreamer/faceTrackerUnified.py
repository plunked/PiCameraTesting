from __future__ import print_function
import argparse
import time
from facedetector import FaceDetector
from camstream import camStream
import cv2

#constructing argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required=True, help="path to the face cascade")
ap.add_argument("-p", "--picam", type=int, default=-1, help="use PiCam instead")
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())


camera = camStream(usePiCamera=args["picam"] > 0).start()
time.sleep(2.0)
print("test init")
#constructing the detector
fd = FaceDetector(args["face"])

print("test0")

while True:
    for frames in camera.read():
        frame = frames.array
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faceRects = fd.detect(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        frameClone = frame.copy()
        print("test1")

        for (fX, fY, fW, fH) in faceRects:
            cv2.rectangle(frameClone, (fX, fY), (fX+fW, fY+fH), (0, 255, 0), 2)

        cv2.imshow("Face", frameClone)
        camera.rawCapture.truncate(0)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
