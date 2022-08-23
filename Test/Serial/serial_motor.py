import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import serial
import datetime

"""
程式不斷給arduino前進的訊號 一直前進
(觀察有沒有卡頓 若有則改變time.sleep或delay
"""
serialCom = '/dev/ttyACM0'
ser = serial.Serial(serialCom, 9600)

def Num2Str(num):
    if str(type(num)) == "<class 'int'>":
        converted = str(num)
        if len(converted) > 3:
            print("Error: invalid num length\nlen:",len(converted))
            return "!!!"
        if len(converted) == 1:
            converted = "00" + converted
        if len(converted) == 2:
            converted = "0" + converted
        return str(converted)
    else:
        print("Error: not int\ndatatype:",type(num))
        return "!!!"

def write_Serial(sender=0,state=0,power=0,motion=0,pwmL=0,pwmR=0,ledA=0,ledB=0,ledC=0,ledD=0):
    pwmL = Num2Str(pwmL)
    pwmR = Num2Str(pwmR)
    signalStr = str(sender) + str(state) + str(power) + str(motion)
    signalStr += str(pwmL) + str(pwmR) + str(ledA) + str(ledB) + str(ledC) + str(ledD)
    try:
        print("Start writing serial...")
        inputStr = str(signalStr) + str('e')
        if len(inputStr) == 15:
            print("py write:",inputStr)
            ser.write(str.encode(inputStr))  
            time.sleep(0.005)   
        else:
            print("Error: serial inputStr length:",len(inputStr))
           
    except KeyboardInterrupt:
        ser.close()
        print("keyboard interrupted!")



camera_port = 0
cap = cv2.VideoCapture(camera_port,cv2.CAP_DSHOW) # cap = cv2.VideoCapture(cv2.CAP_DSHOW + camera_port)

if camera_port == 0:   # notebook camera
    #cap.set(cv2.CAP_PROP_EXPOSURE,-4)
    #cap.set(cv2.CAP_PROP_CONTRAST,0)
    print("Contrast:",cap.get(cv2.CAP_PROP_CONTRAST))
    print("Exposure:",cap.get(cv2.CAP_PROP_EXPOSURE))
    
if camera_port == 1:  # usb camera
    cap.set(cv2.CAP_PROP_EXPOSURE,-7)
    cap.set(cv2.CAP_PROP_CONTRAST,10)
    print("Contrast:",cap.get(cv2.CAP_PROP_CONTRAST))
    print("Exposure:",cap.get(cv2.CAP_PROP_EXPOSURE))

print("Start capturing video from the camera")

if cap.isOpened() == False:
    print("Error: Failed to read the video stream")
else:
    print("Read images successfully\n")

while cap.isOpened():  # Capture frame-by-frame
    ret, frame = cap.read()

    cv2.imshow("original",frame)
    if ret == True: 
        start = datetime.datetime.now()
        
        write_Serial(1,1,1,0,60,60,1,0,0,0)
    
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break
        
        end = datetime.datetime.now()
        print("process time：", end - start)  # 0.2sec / process each frame
        time.sleep(0.02)  # sleep 0.02sec / each frame
        
        # sleep = datetime.datetime.now()
        # print("sleep time：", sleep - end)
    else:
        print("Error: no ret")
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
