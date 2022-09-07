from telnetlib import ECHO
import serial
import time
import sys

COM_PORT = 'COM5'
ser = serial.Serial(COM_PORT, 9600)
inputStr = "A110000000000e"

try:
    while True:
        print("py input:",inputStr)
        ser.write(str.encode(inputStr))  
        time.sleep(0.5)  

        while ser.in_waiting:
            #print('serial in waiting')

            echoStr = str(ser.readline().decode()).strip(' ').strip('\n')
            #print(str(echoStr))
            #print("len",len(str(echoStr)))
            if echoStr[0]=='P': 
                 print('From arduino:', echoStr)
                 if echoStr[1] == '1':
                    stageChanged = int(echoStr[2])
                    print("Change stage to:",stageChanged)

            if echoStr[0]=='D':
                print("\n-----")
                print("debug:",echoStr[1:])
                print("-----\n")

except KeyboardInterrupt:
    ser.close()
    print('bye！')