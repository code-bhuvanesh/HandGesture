import time

import cv2
import pyautogui

print(cv2.__version__)

class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2,tol1=.5,tol2=.5):
        self.hands=self.mp.solutions.hands.Hands(False,maxHands,1,tol1,tol2)
    def Marks(self,frame):
        myHands=[]
        handsType=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            #print(results.multi_handedness)
            for hand in results.multi_handedness:
                #print(hand)
                #print(hand.classification)
                #print(hand.classification[0])
                handType=hand.classification[0].label
                handsType.append(handType)
                print(handsType)
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands,handsType

width=640
height=480
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
findHands=mpHands(2)
pTime = 0
while True:
    ignore,  frame = cam.read()
    frame=cv2.resize(frame,(width,height))
    handData, handsType=findHands.Marks(frame)

    # show FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    for hand,handType in zip(handData,handsType):
        if handType=='Left':
            # print(hand)
            wTip, wPip = hand[8][1], hand[5][1]
            sTip, sPip = hand[12][1], hand[9][1]
            if wTip > wPip:
                print("w")
                pyautogui.keyDown("w")
            else:
                pyautogui.keyUp("w")
            if sTip > sPip:
                print("s")
                pyautogui.keyDown("s")
            else:
                pyautogui.keyUp("s")
        if handType=='Right':
            aTip, aPip = hand[8][1], hand[5][1]
            dTip, dPip = hand[12][1], hand[9][1]
            if aTip > aPip:
                print("a")
                pyautogui.keyDown("a")
            else:
                pyautogui.keyUp("a")
            if dTip > dPip:
                print("d")
                pyautogui.keyDown("d")
            else:
                pyautogui.keyUp("d")

    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()

if __name__ == "__main__":
    mpHands()

