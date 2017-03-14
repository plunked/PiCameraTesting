import numpy as np
import argparse
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "path to the optional video file")
args = vars.(ap.parse_args())

blueLower