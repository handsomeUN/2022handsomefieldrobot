from telnetlib import ECHO
from unittest import result
import serial
import time
import sys
import util
import cv2


COM_PORT = 'COM6'
ser = serial.Serial(COM_PORT, 9600)
STAGE = 2
STATE = 1
pwmL = 0
pwmR = 0
frontCamLED = 0
sideCamLED = 0
Stepper = 0
Pump = 0


def write_serial(receiver='A',stage=0,state=0,pwm_L=0,pwm_R=0,fCam=0,sCam=0,stepper=0,pump=0):
    Py_input = str(receiver) + str(stage) + str(state) + util.Num2Str(pwm_L) + util.Num2Str(pwm_R)
    Py_input += str(fCam) + str(sCam) + str(stepper) + str(pump) + str("e")
    try:
        if len(Py_input) == 14:
            print("From py:",Py_input)
            ser.write(str.encode(Py_input))
    except:
        print("\n\nwrite serial error\n\n")


SIGN_COLOR = 'null'

try:
    frontCam = cv2.VideoCapture(0)
    sideCam = cv2.VideoCapture(1)
    
    while True:

        time.sleep(1)

        print("\nSTAGE:",STAGE)
        print("STATE:",STATE)

        """ For each STAGE, STATE """
        if STAGE == 0: #STOP
            pass
        if STAGE == 1: #N1
            
            if STATE == 1: # TRACK
                write_serial('A',1,1)
                
                #cv2.imshow("result",frame)
                driftCount = 0
                for i in range(10):
                    ret, frame = frontCam.read()
                    if not ret:
                        print("Cannot cap!!!")
                        break
                    DRIFT, result = util.recognition(frame,1,"Tri_R")
                    #print(DRIFT)
                    if DRIFT:
                        driftCount+=1
                
                
                if driftCount>=8:
                    print("\n\n\nStart DRIFTing!!!\n\n\n")
                    STAGE = 1
                    STATE = 3
                
                
            if STATE == 3: # DRIFT
                write_serial('A',1,3)

            if STATE == 9: # SWITCH
                write_serial('A',1,9)
                time.sleep(3)
                STAGE = 2
                STATE = 1
                
        if STAGE == 2: #N2
            
            if STATE == 1: # TRACK
                write_serial('A',2,1)
                
                ColorCount=0
                SIGN_Color='null'
                for i in range(10):
                    ret, frame = sideCam.read()
                    if not ret:
                        print("Cannot cap!!!")
                        break
                    
                    SIGN_Color = util.color_sign_recog(frame)
                    #print(SIGN_Color)
                    if SIGN_Color!='null':
                        ColorCount+=1
                
                
                if ColorCount>=8:
                    print("\n\n\nFind Sign:",SIGN_Color,"\n\n\n")
                    SIGN_COLOR = SIGN_Color
                    STAGE = 2
                    STATE = 'S'
                    
                
            if STATE == 'S': # SIGN
                C = 'n'
                if SIGN_COLOR == 'red':
                    C = 'R'
                if SIGN_COLOR == 'yellow':
                    C = 'Y'
                if SIGN_COLOR == 'blue':
                    C = 'B'
                if SIGN_COLOR == 'black':
                    C = 'K'
                
                write_serial('A',2,'S',0,0,0,C)
                time.sleep(4)
                STAGE = 2
                STATE = 'F'
                
                
            if STATE == 'F': # FRUIT
                write_serial('A',2,'F')
                
                
            if STATE == 'G': # GRAB
                write_serial('A',2,'G')
                
            if STATE == 11: # TRACK
                write_serial('A',2,1)
                time.sleep(20) #TBD
                STAGE = 2
                STATE = 'D'
                
            if STATE == 'D': # DROP
                write_serial('A',2,'D')
                
            if STATE == 12: # TRACK
                write_serial('A',2,1)
                """ 通過關卡線直到撞牆"""
            
                
                
            
            
            
            
        if STAGE == 3: #N3
            write_serial('A',3,1)
        if STAGE == 4: #T1
            pass
        if STAGE == 5: #T2
            pass
        if STAGE == 6: #T3
            pass
        if STAGE == 7: #U
            pass


        """ Receive messages """
        while ser.in_waiting:
            time.sleep(0.4)
            #print('serial in waiting')
            echoStr = str(ser.readline().decode()).strip(' ').strip('\n')
            #print(str(echoStr))
            Receiver = echoStr[0]
            if_STAGE_changed = echoStr[1]
            STAGE_changed = echoStr[2]
            if_STATE_changed = echoStr[3]
            STATE_changed = echoStr[4]
            
            if Receiver=='P': # Arduino -> Python 
                print('From arduino:', echoStr)
                if if_STAGE_changed == '1': # button pressed, STAGE changed
                    #print("Change stage to:",STAGE_changed)
                    STAGE = int(STAGE_changed)
                    #STATE = 0
                if if_STATE_changed == '1': # STATE changed
                    #print("Change state to:",STATE_changed)
                    STATE = int(STATE_changed)

            if Receiver=='D': # Arduino debug messages
                print("\n-----")
                print("From debug:",echoStr[2:])
                print("-----\n")
                
        """ Write messages to Arduino""" 
        #print("start writing serial...")
        write_serial('A',STAGE,STATE,pwmL,pwmR,frontCamLED,sideCamLED,Stepper,Pump)

except KeyboardInterrupt:
    ser.close()
    print('bye！')






