#learning to access the PiCamera using OpenCV

#importing packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#initializing camera and grab a reference
camera = PiCamera()
rawCapture = PiRGBArray(camera)

#allow camera to warmup
time.sleep(0.1)

#grab image
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

#display image onscreen
cv2.imshow("Image", image)
cv2.waitKey(0)
