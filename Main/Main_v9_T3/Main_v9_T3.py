from telnetlib import ECHO
from unittest import result
import serial
import time
import sys
import cv2
import util

NX = False
FrontCam_port = 2
SideCam_port = 1


if NX:
    COM_PORT = 'dev/ttyACM0'
else:
    COM_PORT = '/dev/cu.usbmodem1'
    
ser = serial.Serial(COM_PORT, 9600)
STAGE = 6
STATE = 1
pwmL = 0
pwmR = 0
frontCamLED = 0
sideCamLED = 0
Stepper = 0
Pump = 0
SIGN_COLOR = 'null'


def write_serial(receiver='A',stage=0,state=0,pwm_L=0,pwm_R=0,fCam=0,sCam=0,stepper=0,pump=0):
    Py_input = str(receiver) + str(stage) + str(state) + util.Num2Str(pwm_L) + util.Num2Str(pwm_R)
    Py_input += str(fCam) + str(sCam) + str(stepper) + str(pump) + str("e")
    try:
        if len(Py_input) == 14:
            print("From py:",Py_input)
            ser.write(str.encode(Py_input))
    except:
        print("\n\nwrite serial error\n\n")



try:
    """
    frontCam = cv2.VideoCapture(1)
    sideCam = cv2.VideoCapture(2)
    """
    
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
            pass
        if STAGE == 6: #T3
            if STATE == 1: # TRACK
                write_serial('A',6,1)
                
                driftCount = 0
                Camera.release()
                Camera = cv2.VideoCapture(FrontCam_port)
                for i in range(10):
                    ret, frame = Camera.read()
                    if not ret:
                        print("Cannot cap!!!")
                        break
                    DRIFT, result = util.recognition(frame,1,"Rec")
                    #print(DRIFT)
                    if DRIFT:
                        driftCount+=1
                
                if driftCount>=8:
                    print("\n\n\nStart DRIFTing!!!\n\n\n")
                    STAGE = 6
                    STATE = 3
               
            if STATE == 3: # DRIFT
                write_serial('A',6,3)

            # if STATE == 9: # SWITCH
            #     write_serial('A',1,9)
            #     time.sleep(3)
            #     STAGE = 2
            #     STATE = 6
            #     continue
        
        if STAGE == 7: #U
            pass

        """ Receive messages """
        while ser.in_waiting:
            time.sleep(0.4)
            #print('serial in waiting')
            echoStr = str(ser.readline().decode()).strip(' ').strip('\n')
            #print(str(echoStr))
            
            try: 
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
                        if STAGE==1: #N1
                            STATE = 1
                        if STAGE==2: #N2
                            STATE = 6
                        if STAGE==3: #N3
                            STATE = 3
                            """ TBD """
 
                    if if_STATE_changed == '1': # STATE changed
                        #print("Change state to:",STATE_changed)
                        STATE = int(STATE_changed)

                if Receiver=='D': # Arduino debug messages
                    print("\n-----")
                    print("From debug:",echoStr[2:])
                    print("-----\n")
            except:
                pass
                        
        """ Write messages to Arduino""" 
        #print("start writing serial...")
        #write_serial('A',STAGE,STATE,pwmL,pwmR,frontCamLED,sideCamLED,Stepper,Pump)

    
except KeyboardInterrupt:
    cv2.destroyAllWindows()
    ser.close()
    print('bye！')





