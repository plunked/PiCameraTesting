import cv2 

image = cv2.imread("test.png", cv2.CV_LOAD_IMAGE_GRAYSCALE)
cv2.imwrite("Image", image)

