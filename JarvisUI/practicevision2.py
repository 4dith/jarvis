import cv2
import mediapipe as mp
import pyautogui
import random
import util
import time
import numpy as np

hover_start_time = 0
hover_threshold = 1.0  # seconds required to trigger hover click
hover_target = None

from pynput.mouse import Button, Controller
mouse = Controller()


screen_width, screen_height = pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

prev_thumb_index_dist = None
def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
        index_finger_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return index_finger_tip
    return None, None
screen_width, screen_height = pyautogui.size()

def move_mouse(index_finger_tip, winW, winH):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * winW)
        y = int(index_finger_tip.y * winH)
        # Clamp inside Pygame window
        x = max(0, min(x, winW))
        y = max(0, min(y, winH))
        return (x, y)
    return None

def is_left_click(landmark_list, thumb_index_dist):
             return thumb_index_dist < 100


def is_right_click(landmark_list, thumb_index_dist):
    return (
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90  and
            thumb_index_dist > 50
    )


def is_double_click(landmark_list, thumb_index_dist):
    return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            thumb_index_dist > 50
    )
def hover_click(hand_pos, buttons):
    """
    hand_pos : (x, y) of hand cursor
    buttons : list of AppButton or any object with isOver() method
    Returns: button clicked if hover is completed, else None
    """
    global hover_start_time, hover_target

    if hand_pos is None:
        hover_start_time = 0
        hover_target = None
        return None

    # check which button is currently hovered
    current_target = None
    for btn in buttons:
        if btn.isOver(hand_pos):
            current_target = btn
            break

    if current_target is None:
        # not hovering any button
        hover_start_time = 0
        hover_target = None
        return None

    if hover_target != current_target:
        # new hover target, reset timer
        hover_target = current_target
        hover_start_time = time.time()
        return None

    # calculate hover duration
    elapsed = time.time() - hover_start_time
    if elapsed >= hover_threshold:
        hover_start_time = 0  # reset after click
        return current_target  # trigger click

    return None

def is_screenshot(landmark_list, thumb_index_dist):
    return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            thumb_index_dist < 50
    )


def detect_gesture(landmark_list):
    if len(landmark_list) < 21:
        return None

    # calculate thumb_index_dist
    thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[8]])  # thumb tip to index tip

    if is_left_click(landmark_list, thumb_index_dist):
        return "left_click"
    elif is_right_click(landmark_list, thumb_index_dist):
        return "right_click"
    elif is_double_click(landmark_list, thumb_index_dist):
        return "double_click"
    elif is_screenshot(landmark_list, thumb_index_dist):
        return "screenshot"
    else:
        return None
    

def main():
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_gesture(frame, landmark_list, processed)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
