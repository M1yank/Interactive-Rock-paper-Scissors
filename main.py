from random import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap=cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

### hand detector
detector= HandDetector(maxHands=1)


timer = 0
stateResult = False
startGame = False
scores = [0,0]


while True:
    imgBG = cv2.imread('Resources/dock.png')  
    success, img = cap.read()
    imgScaled = cv2.resize(img, (0,0), None, 0.63125, 0.63125)  #resize height of cam
    imgScaled = imgScaled[:,51:353]                             #crop width of cam
    hands, img = detector.findHands(imgScaled)

    if startGame:
        
        if stateResult is False:
            timer = time.time() - InitialTime
            cv2.putText(imgBG, str(int(timer)), (450, 340), cv2.FONT_HERSHEY_PLAIN, 6, (0,0,0), 4)
            if timer>3:
                stateResult = True
                timer = 0 

                if hands:
                    hand=hands[0]
                    playerMove = None
                    fingers = detector.fingersUp(hand)

                    if fingers==[0, 0, 0, 0, 0]:    #rock
                        playerMove = 1
                    if fingers==[1, 1, 1, 1, 1]:    #paper
                        playerMove = 2
                    if fingers==[0, 1, 1, 0, 0]:    #scissor
                        playerMove = 3


                    randomNumber =  random.randint(1, 3)
                    imgAI=cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED);
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (60, 180))

                    # Draw
                    if playerMove == randomNumber:
                        cv2.putText(imgBG, str('DRAW'), (410, 180), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)

                    # Player wins:
                    if(playerMove==1 and randomNumber==3) or (playerMove==2 and randomNumber==1) or (playerMove==3 and randomNumber==2):
                        scores[1] += 1
                    
                    # AI Wins:
                    if(randomNumber==1 and playerMove==3) or (randomNumber==2 and playerMove==1) or (randomNumber==3 and playerMove==2):
                        scores[0] += 1
                    


    #embed cam into background image
    imgBG[178:481, 596:898] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (60, 180))      


    cv2.putText(imgBG, str(int(scores[0])), (280, 160), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 2)
    cv2.putText(imgBG, str(int(scores[1])), (640, 160), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 2)

    cv2.putText(imgBG, str('Press S to start'), (410, 140), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)
    cv2.putText(imgBG, str('Press X to start'), (410, 160), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)

    cv2.imshow("BG", imgBG)
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        InitialTime = time.time()
        stateResult = False   

    if key == ord('x'):
        startGame = False
        break

cv2.destroyAllWindows()

    
