import cv2
import numpy as np

img = np.zeros((512,512, 3), np.uint8) #Black
#print(img.shape)
#img[:] = 255,0,0 # Blue

cv2.line(img, (0,0), (img.shape[1],img.shape[0]), (0,255,255), thickness=3)
cv2.rectangle(img, (0,0), (250,350), (0,255,0), cv2.FILLED) # cv2.FILLED replaces the thickness parameter
cv2.circle(img, (450,450), 30, (0,0,250), thickness=2)
cv2.putText(img, "OPENCV", (100,200), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), thickness=1)

cv2.imshow("Image", img)
cv2.waitKey(0)