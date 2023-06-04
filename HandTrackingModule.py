import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode, maxHands, min_detection_confidence=detectionCon,
                                        min_tracking_confidence=trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB.flags.writeable = False
        self.results = self.hands.process(imgRGB)
        imgRGB.flags.writeable = True

        # print(self.results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPositions(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (0, 0, 200), cv2.FILLED)
        return lmList

    def findHandPositions(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            handsType = list()
            for hand in self.results.multi_handedness:
                # print(hand)
                # print(hand.classification)
                # print(hand.classification[0])
                handType = hand.classification[0].label
                handsType.append(handType)

            myHand = self.results.multi_hand_landmarks[handNo]
            for id, (lm, handLabel) in enumerate(zip(myHand.landmark, handsType)):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([handLabel, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (0, 0, 200), cv2.FILLED)
        return lmList
