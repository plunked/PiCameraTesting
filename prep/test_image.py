from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

piCam = PiCamera()
rawCapture = PiRGBArray(piCam)

#allow camera to warmup
time.sleep(0.1)

#grab image
piCam.capture(rawCapture, format="bgr")
image = rawCapture.array

#display image onscreen
cv2.imshow("Image", image)
cv2.waitKey(0)
