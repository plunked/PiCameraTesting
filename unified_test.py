from camStream import camStream
import argparse
import time
#import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picam", type=int, default=-1, help="whether or not the Raspbery Pi camera should be used")
args = vars(ap.parse_args())

videoStream = camStream(usePiCam=args["picam"] > 0).start()
time.sleep(2.0)

while True:
    frame = videoStream.read()
    #frame = imutils.resize(frame, width=400)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()
videoStream.stop()