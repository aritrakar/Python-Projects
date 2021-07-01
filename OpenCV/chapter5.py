import cv2
import numpy as np

img = cv2.imread("Resources/cards.jpg")
print(img.shape)

width, height = 250,350
pts1 = np.float32([[956,39],[1243,39],[956,445], [1243,445]])
pts2 = np.float32([[0,0],[width, 0],[0, height],[width, height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
imgOutput = cv2.warpPerspective(img, matrix, (width, height))

cv2.imshow("Image", img)
cv2.imshow("Image output", imgOutput)
cv2.waitKey(0)