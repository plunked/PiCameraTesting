from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="path to the JSON configuration file")
args = vars(ap.parse_args())
 
# filter warnings, load the configuration and initialize the Dropbox
# client
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))
client = None

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.framerate = conf["fps"]
rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))

# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print ("[INFO] warming up...")
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0

# capture frames from the camera
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image and initialize
	# the timestamp and occupied/unoccupied text
    frame = f.array
    timestamp = datetime.datetime.now()
    text = "Unoccupied"

	# resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the average frame is None, initialize it
    if avg is None:
        print ("[INFO] starting background model...")
        avg = gray.copy().astype("float")
        rawCapture.truncate(0)
        continue
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
    
    thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in cnts:
        if cv2.contourArea(c) < conf["min_area"]:
            continue

        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"
        
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        
    if text == "Occupied":
        if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
            motionCounter += 1
            
            if motionCounter >= conf["min_motion_frames"]:
                if conf["use_dropbox"]:
                    t = TempImage()
                    cv2.imwrite(t.path, frame)
                    print "[UPLOAD] {}".format(ts)
                    path = "{base_path}/{timestamp}.jpg".format(base_path=conf["dropbox_base_path"], timestamp=ts)
                    client.put_file(path, open(t.path, "rb"))
                    t.cleanup()
                lastUploaded = timestamp
                motionCounter = 0

	# otherwise, the room is not occupied
    else:
        motionCounter = 0

    # check to see if the frames should be displayed to screen
    if conf["show_video"]:
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF
        
    if key == ord("q"):
        break

	# clear the stream in preparation for the next frame
    rawCapture.truncate(0)
