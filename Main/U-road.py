from tokenize import _all_string_prefixes
import numpy as np
import cv2

from telnetlib import ECHO
import serial
import time
import sys

COM_PORT = 'COM6'
ser = serial.Serial(COM_PORT, 9600)


def u_road(frame):
    pwm = ('150', '150')
    middle = 320
    pipe_lower = np.array([0,102,133])   
    pipe_upper = np.array([20,255,255]) 

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (15, 15), 0)
    hsv = hsv[0:,480:]

    pipe_mask = cv2.inRange(hsv, pipe_lower, pipe_upper) 
    pipe_mask = cv2.erode(pipe_mask, None, iterations=2)
    pipe_mask = cv2.dilate(pipe_mask, None, iterations=2)

    pipe_contours, pipe_hierarchy= cv2.findContours(pipe_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(pipe_contours) > 0:
        pipe_cnt = max(pipe_contours, key=cv2.contourArea)
        pipe_output = cv2.bitwise_and(hsv, hsv, mask = pipe_mask)

        M = cv2.moments(pipe_cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(pipe_output, (cX, cY), 1, (255, 255, 255), 4)
        cv2.imshow('pipe', pipe_output)

        if cY > middle+5:
            #turn left
            pwm = ('-05', '050')
            print('turn left')
            return pwm
        elif cY < middle-5:
            #turn right
            pwm = ('050','-05')
            print('turn right')
            return pwm
            
    return pwm


cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    pwm = u_road(frame)
    if cv2.waitKey(1) == ord('Q'):
        ser.close()
        break
    print(pwm)
    u_serial = 'A00' + pwm[0] + pwm[1] + '0000e'
    print(u_serial)
    #ser.write(str.encode(u_serial))
    ser.write(str.encode("A001501500000e"))
    # write_serial('A', 7, 'U', pwm_L=pwm[0], pwm_R=pwm[1])
cap.release()
cv2.destroyAllWindows()