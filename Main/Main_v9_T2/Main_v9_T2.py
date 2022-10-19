from platform import release
from sre_parse import State
from telnetlib import ECHO
from unittest import result
import serial
import time
import sys
import util
import cv2

NX = False
FrontCam_port = 2
SideCam_port = 1

if NX:
    COM_PORT = 'dev/ttyACM0'
else:
    COM_PORT = '/dev/cu.usbmodem14101'

ser = serial.Serial(COM_PORT, 9600)
STAGE = 5
STATE = 4
pwmL = 0
pwmR = 0
frontCamLED = 0
sideCamLED = 0
Stepper = 0
Pump = 0
water = True


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
    # frontCam = cv2.VideoCapture(0)
    # sideCam = cv2.VideoCapture(1)
    Camera = cv2.VideoCapture(FrontCam_port)

    while True:

        time.sleep(1)

        print("\nSTAGE:",STAGE)
        print("STATE:",STATE)

        """ For each STAGE, STATE """
        if STAGE == 0: #STOP
            pass
        if STAGE == 1: #N1
            pass
        if STAGE == 2: #N2
            pass            
        if STAGE == 3: #N3
            pass
        if STAGE == 4: #T1
            pass
        if STAGE == 5: #T2
            if STATE == 1: #TRACK
                write_serial('A',5,1)
                
                ColorCount=0
                SIGN_Color='null'

                Camera.release()
                Camera = cv2.VideoCapture(SideCam_port)

                for i in range(10):
                    ret, frame = Camera.read()
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
                    STAGE = 5
                    STATE = 2
                    
            if STATE == 2: # SIGN
                C = 'n'
                if SIGN_COLOR == 'red':
                    C = 'R'
                if SIGN_COLOR == 'yellow':
                    C = 'Y'
                if SIGN_COLOR == 'blue':
                    C = 'B'
                if SIGN_COLOR == 'black':
                    C = 'K'
                
                write_serial('A',5,2,0,0,0,C)
                time.sleep(4)
                STAGE = 5
                STATE = 3


            if STATE == 3: # FindCase
                write_serial('A',5,3)
                # Camera.release()
                ret, frame = Camera.read()
                if not ret:
                    print("Cannot cap!!!")
                    break
                
                max_x1, min_y1, max_x2, max_y2 = util.take_shower(frame)
                print("maxx2:",max_x2)
                if max_x2 < 1200 and max_x2 > 1000 and SIGN_COLOR == 'red':
                    print("reach red!!")
                    write_serial('A',5,3,0,0,0,'Y')
                    STATE = 4
                    
                elif max_x2 < 500 and max_x2 > 470 and SIGN_COLOR == 'yellow':
                    print("reach yellow!!")
                    write_serial('A',5,3,0,0,0,'Y')
                    STATE = 4

                elif max_x2 < 220 and max_x2 > 200 and SIGN_COLOR == 'blue':
                    print("reach blue!!")
                    write_serial('A',5,3,0,0,0,'Y')
                    STATE = 4
                    
                elif max_x2 < 220 and max_x2 > 200 and SIGN_COLOR == 'black':
                    print("reach black!!")
                    write_serial('A',5,3,0,0,0,'Y')
                    STATE = 4
                        

            if STATE == 4:
                SIGN_COLOR = 'red'

                if SIGN_COLOR == 'yellow' or SIGN_COLOR == 'black':
                    write_serial('A',5,4,0,0,0,0,1) #extend the stepper to reach yellow or black
                    time.sleep(10)
                
                if water==True:
                    write_serial('A',5,4,0,0,0) #pee 38s 
                    time.sleep(10)
                    water = False

                if SIGN_COLOR == 'red' or SIGN_COLOR == 'blue':
                    write_serial('A',5,4,0,0,0,0,2) #retract the stepper (short retract)
                    time.sleep(10)
                    STATE = 5
                if SIGN_COLOR == 'yellow' or SIGN_COLOR == 'black':
                    write_serial('A',5,4,0,0,0,0,3) #retract the stepper (long retract)
                    time.sleep(15)
                    STATE = 5
                
            if STATE == 5: #TRACK
                write_serial('A',5,5,0,0,0)

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
        # write_serial('A',STAGE,STATE,pwmL,pwmR,frontCamLED,sideCamLED,Stepper,Pump)

except KeyboardInterrupt:
    ser.close()
    print('bye！')





