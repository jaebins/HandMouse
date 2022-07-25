import asyncio
import threading
import cv2
import mediapipe as mp
import pyautogui
from tkinter import *

root = Tk()
pyautogui.FAILSAFE = False

# 모니터 해상도
monitor_width = root.winfo_screenheight()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def moveMouse(mouseX, mouseY):
  pyautogui.moveTo(mouseX, mouseY, duration=0.0)

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7 ) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      continue

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:

      for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        
        # 손 위치 가져오기
        fingLoc_8 = hand_landmarks.landmark[8]
        mouseX_8 = int(monitor_width - hand_landmarks.landmark[8].x * 1000)
        mouseY_8 = int(hand_landmarks.landmark[8].y * 1000)
        mouseZ_8 = int(hand_landmarks.landmark[8].z * 1000)

        FingLoc_4 = hand_landmarks.landmark[4]
        mouseX_4 = int(monitor_width - hand_landmarks.landmark[4].x * 1000)
        mouseY_4 = int(hand_landmarks.landmark[4].y * 1000)
        mouseZ_4 = int(hand_landmarks.landmark[4].z * 1000)

        FingLoc_12 = hand_landmarks.landmark[12]
        mouseX_12 = int(monitor_width - hand_landmarks.landmark[12].x * 1000)
        mouseY_12 = int(hand_landmarks.landmark[12].y * 1000)
        mouseZ_12 = int(hand_landmarks.landmark[12].z * 1000)

        FingLoc_16 = hand_landmarks.landmark[16]
        mouseX_16 = int(monitor_width - hand_landmarks.landmark[16].x * 1000)
        mouseY_16 = int(hand_landmarks.landmark[16].y * 1000)
        mouseZ_16 = int(hand_landmarks.landmark[16].z * 1000)

        # 움직임 이벤트
        t = threading.Thread(moveMouse(mouseX_8, mouseY_8))
        t.start()

        # 좌클릭 이벤트0
        clickDirX_Left = (mouseX_8**2 + mouseX_4**2)**(1/2)
        clickDirY_Left = (mouseY_8**2 + mouseY_4**2)**(1/2)
        clickDirZ_Left = (mouseZ_8**2 + mouseZ_4**2)**(1/2) # 실제 계싼 값
        print("%04.2f,\t%04.2f,\t%04.2f"%(clickDirX_Left, clickDirY_Left, clickDirZ_Left))
        if(clickDirZ_Left < 50):
          pyautogui.click()
          print("좌클릭")

        # # 더블클릭 이벤트
        # clickDir_DoubleCLick = (mouseY_12^2 + mouseY_4^2)**(1/2)
        # if(clickDir_DoubleCLick < 10):
        #   pyautogui.doubleClick()
        #   print("더블클릭")

        # # 우클릭 이벤트
        # clickDir_Right = (mouseY_16^2 + mouseY_4^2)**(1/2)
        # if(clickDir_Right < 10):
        #   pyautogui.rightClick()
        #   print("우클릭")

        break

    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()