from djitellopy import tello
import cv2
import numpy as np
import time

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

drone.streamon()

cap = cv2.drone.get_frame_read().frame

while(1):
    ret, frame = cap.read()     #   카메라 모듈 연속프레임 읽기

    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    # BGR을 HSV로 변환해줌


    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=blue_mask)      # 흰색 영역에 파랑색 마스크를 씌워줌.
    res1 = cv2.bitwise_and(frame, frame, mask=green_mask)    # 흰색 영역에 초록색 마스크를 씌워줌.
    res2 = cv2.bitwise_and(frame, frame, mask=red_mask)    # 흰색 영역에 빨강색 마스크를 씌워줌.

    cv2.imshow('frame',frame)       # 원본 영상을 보여줌
    cv2.imshow('Blue', res)           # 마스크 위에 파랑색을 씌운 것을 보여줌.
    cv2.imshow('Green', res1)          # 마스크 위에 초록색을 씌운 것을 보여줌.
    cv2.imshow('red', res2)          # 마스크 위에 빨강색을 씌운 것을 보여줌.

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

while True:
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (1200, 800))
    cv2.imshow("Image", img)
    cv2.waitKey(1)

cv2.destroyAllWindows()
