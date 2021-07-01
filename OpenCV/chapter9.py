import cv2

faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
# img = cv2.imread("Resources/image.png")
# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
#
# for (x,y,width,height) in faces:
#     cv2.rectangle(img, (x,y), (x+width, y+height), (255,0,0), 2)
#
# cv2.imshow("Result", img)
# cv2.waitKey(0)

cap = cv2.VideoCapture(0)
cap.set(3, 1080)
cap.set(4, 720)
cap.set(10,100)

while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, width, height) in faces:
        cv2.rectangle(img, (x,y), (x+width, y+height), (255,0,0), 2)

    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break