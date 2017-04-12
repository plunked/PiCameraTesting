import cv2

class FaceDetector:
    def __init__(self, faceCascadePath):
        self.faceCascade = cv2.CascadeClassifier(faceCascadePath)

    def detect(self, image, scaleFactor = 1.1, minNeighbors = 5, minSize = (30, 30)):
        rects = self.faceCascade.detectMultiScale(image, 
        scaleFactor = scaleFactor, 
        minNeighbors = minNeighbors, 
        minSize = minSize, 
        flags = cv2.CASCADE_SCALE_IMAGE)
        return rects

    #scaleFactor refers to how much the image size is reduced at each image scale.
    # Used to create the scale pyramid in order to detect faces at multiple scales in the image.
    # minNeighbors is the number of neighbors each window should have in order
    # to be considered a face.
    # minSize dictates the minimum size of the window.
