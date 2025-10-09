import cv2
import mediapipe as mp
import pygame
from time import time


class HandCursor:
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1)
    mpDraw = mp.solutions.drawing_utils
    cap = None

    def __init__(self, radius, color, winW, winH, imageFraction=1, clickTime=1) -> None:
        self.enabled = False
        self.position = None
        self.radius = radius
        self.color = color
        self.winW = winW
        self.winH = winH
        self.imageFraction = imageFraction
        self.clickTime = clickTime

        self.imgW = 0
        self.imgH = 0
        self.remainingClickTime = clickTime
        self.prevTime = None
        self.selectedWidget = None

        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=1
        )

        # Gesture-related attributes
        self.landmark_list = []
        self.index_finger_tip = None
        self.frame = None
        self.processed = None

    def enable(self):
        self.enabled = True

        self.cap = cv2.VideoCapture(0)
        success, img = self.cap.read()
        if success:
            self.imgH, self.imgW, _ = img.shape

    def disable(self):
        self.enabled = False
        self.position = None
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.cap = None
        self.imgW = self.imgH = 0
    
    def shouldClick(self, widget):
        if widget != self.selectedWidget:
            self.selectedWidget = widget
            self.remainingClickTime = self.clickTime
            self.prevTime = time()
            return False
        else:
            currentTime = time()
            self.remainingClickTime -= currentTime - self.prevTime
            if self.remainingClickTime > 0:
                self.prevTime = currentTime
                return False
            else:
                self.selectedWidget = self.prevTime = None
                return True

    def updatePos(self, showImage=False):
        if not self.enabled or self.cap is None:
            return

        success, img = self.cap.read()
        if not success:
            return
        self.frame = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.processed = self.hands.process(imgRGB)

        self.position = None
        self.landmark_list = []
        self.index_finger_tip = None

        if self.processed.multi_hand_landmarks:
            handLms = self.processed.multi_hand_landmarks[0]
            self.index_finger_tip = handLms.landmark[self.mpHands.HandLandmark.MIDDLE_FINGER_TIP]

            # Store all landmarks
            for lm in handLms.landmark:
                self.landmark_list.append((lm.x, lm.y))

            # Compute cursor position
            minFrac = (1 - self.imageFraction) / 2
            maxFrac = 1 - minFrac

            bx, by = min(max(minFrac, self.index_finger_tip.x), maxFrac), min(max(minFrac, self.index_finger_tip.y), maxFrac)
            sx, sy = (bx - minFrac) / (maxFrac - minFrac), (by - minFrac) / (maxFrac - minFrac)
            self.position = int(sx * self.winW), int(sy * self.winH)

            if showImage:
                ix, iy = int(self.index_finger_tip.x * self.imgW), int(self.index_finger_tip.y * self.imgH)
                cv2.circle(self.frame, (ix, iy), 15, (255, 0, 0), cv2.FILLED)
                self.mpDraw.draw_landmarks(self.frame, handLms, self.mpHands.HAND_CONNECTIONS)

        if showImage:
            cv2.imshow("Hand Cursor", self.frame)
    def draw(self, win):
        if self.position:
            pygame.draw.circle(win, self.color, self.position, self.radius)
