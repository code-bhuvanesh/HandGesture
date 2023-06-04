import math
import cv2
import HandTrackingModule as htm
import time
import MoveWindow as moveWindow
import win32gui as gui
import sys


def main():
    cTime = 0
    pTime = 0
    detector = htm.HandDetector()
    hCam, wCam = 720, 1280
    # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    windowCount = 1
    canSwitchWindow = True
    while True:
        try:
            success, img = cap.read()
            img = detector.find_hands(img)
            lmlist = detector.findPositions(img, draw=False)
            if len(lmlist) != 0:
                # print(lmlist[4])
                x1, y1 = lmlist[5][1], lmlist[5][2]
                x2, y2 = lmlist[8][1], lmlist[8][2]
                fTipX, fTipy = lmlist[12][1], lmlist[12][2]
                fPipX, fPipy = lmlist[9][1], lmlist[9][2]

                if is_hand_closed(lmlist) and fTipy < fPipy and canSwitchWindow:
                    try:
                        winList = moveWindow.getWindows()
                        # for win in winList:
                        #     print(gui.GetWindowTextLength(win))
                        print(f"total = {len(winList)}, current len = {windowCount}")

                        moveWindow.switchWindow(winList[windowCount])
                        windowCount += 1
                        if windowCount > (len(winList) - 1):
                            windowCount = 0
                        # time.sleep(0.2)
                        canSwitchWindow = False
                    except OSError:
                        print("error switching window")
                    continue

                if not is_hand_closed(lmlist) and not canSwitchWindow:
                    canSwitchWindow = True

                if fTipy > fPipy:
                    # print("yes")
                    movePosX = x1 - x2
                    movePosY = y1 - y2
                    # print(f"x = ", movePosX)
                    # print(f"y = ", movePosY)
                    # time.sleep(0.001)
                    moveWindow.move_window(movePosX, movePosY, 60)
                # else:
                # print("no")

                cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)

            # show FPS
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

            cv2.imshow("image", img)
            cv2.waitKey(1)
        except:
            print("error")
    cv2.destroyAllWindows()


def is_hand_closed(lmlist):
    if len(lmlist) != 0:
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]

        length = math.hypot(x2-x1, y2-y1)

        if length < 30 :
            print("hand closed")
            return True
    print("hand opened")
    return False


if __name__ == "__main__":
    main()
