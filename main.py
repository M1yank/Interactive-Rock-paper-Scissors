import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap=cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

detector= HandDetector(maxHands=2)

while True:
    #read background image
    imgBG = cv2.imread('Resources/dock.png')
    success, img = cap.read()
    
    #resize height of cam
    imgScaled = cv2.resize(img, (0,0), None, 0.63125, 0.63125)
    
    #crop width of cam
    imgScaled = imgScaled[:,51:353]
    
    #flip the cam
    imgScaled = cv2.flip(imgScaled, 1)

    #find hands
    hands, img = detector.findHands(imgScaled)


    #embed cam into background image
    imgBG[178:481, 596:898] = imgScaled
    cv2.imshow("BG", imgBG)
    cv2.waitKey(1)