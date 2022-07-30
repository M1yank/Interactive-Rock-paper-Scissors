import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

cap=cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

### hand detector
detector= HandDetector(maxHands=1)


timer = 0
stateResult = False
startGame = False



while True:
    #read background image
    imgBG = cv2.imread('Resources/dock.png')
    success, img = cap.read()
    
    #resize height of cam
    imgScaled = cv2.resize(img, (0,0), None, 0.63125, 0.63125)
    
    #crop width of cam
    imgScaled = imgScaled[:,51:353]
    
    #flip the cam
    # imgScaled = cv2.flip(imgScaled, 1)

    #find hands
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
                    fingers = detector.fingersUp(hand)

                    if fingers==[0, 0, 0, 0, 0]:    #rock
                        playerMove = 1
                    if fingers==[1, 1, 1, 1, 1]:    #paper
                        playerMove = 2
                    if fingers==[0, 1, 1, 0, 0]:    #scissor
                        playerMove = 3

                    imgAI=cv2.imread(f'Resources/1.png');
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, ())


                    print(playerMove) 


    #embed cam into background image
    imgBG[178:481, 596:898] = imgScaled
    cv2.imshow("BG", imgBG)
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        InitialTime = time.time()   