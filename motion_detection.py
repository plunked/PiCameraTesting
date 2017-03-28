import argparse 
import datetime
import imutils
import time
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

if args.get("video", None) is None:
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = (32)
    camera.vflip = True
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.25)

else:
    camera = cv2.VideoCapture(args["video"])

firstFrame = None

for frames in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    frame = frames.array
    text = "Unoccupied"
    frame = imutils.resize(frame, width=300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0 )

    if firstFrame is None:
        firstFrame = gray.copy().astype("float")
        rawCapture.truncate(0)
        continue
    cv2.accumulateWeighted(gray, firstFrame, 0.5)      
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(firstFrame))
    thresh = cv2.threshold(frameDelta, 2, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        if cv2.contourArea(c) < args["min_area"]:
            continue

        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"
        cv2.imshow("Feed", frame)
        #cv2.imshow("Thresh", thresh)
        #cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
    rawCapture.truncate(0)
