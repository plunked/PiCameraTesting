from threading import thread
import cv2

class webCamStream:
    def __init__(self, src=0):
        self.camera = cv2.VideoCapture()
        (self.grabbed, self.frame) = self.camera.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update(), args=()).start()
        return self
    
    def update(self):
        while True:
            if self.stopped:
                return
            
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
 