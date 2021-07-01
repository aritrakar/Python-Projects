import cv2
import numpy as np

img = cv2.imread("Resources/image.png")
print(img.shape) # Prints (Height, Width, NO. OF CHANNELS)

imgResize = cv2.resize(img, (400,400)) #Width, Height
print(imgResize.shape)

imgCropped = img[0:200, 200:500] #Height then width

cv2.imshow("Image", img)
#cv2.imshow("Image Resize", imgResize)
cv2.imshow("Image Cropped", imgCropped)
cv2.waitKey(0)