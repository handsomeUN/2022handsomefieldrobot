from telnetlib import ECHO
import serial
import time
import sys

COM_PORT = 'COM5'
ser = serial.Serial(COM_PORT, 9600)
STAGE = 0
STATE = 0
pwmL = 0
pwmR = 0


def Num2Str(num):
    if str(type(num)) == "<class 'int'>":
        cvt = str(num)
        if len(cvt) ==2:
            cvt = "0" + cvt
        if len(cvt) ==1:
            cvt = "00" + cvt

        return str(cvt)
    else:
        return "error"

def write_serial(receiver='A',stage=0,state=0,pwmL=0,pwmR=0,fCam=0,sCam=0,stepper=0,pump=0):
    Py_input = str(receiver) + str(stage) + str(state) + Num2Str(pwmL) + Num2Str(pwmR)
    Py_input += str(fCam) + str(sCam) + str(stepper) + str(pump) + str("e")
    try:
        if len(Py_input) == 14:
            print("From py:",Py_input)
            ser.write(str.encode(Py_input))
    except:
        print("\n\nwrite serial error\n\n")




try:
    while True:

        time.sleep(0.5)

        """ Write messages to Arduino""" 
        #print("start writing serial...")
        write_serial('A',STAGE,STATE,pwmL,pwmR)

        """ Receive messages """
        while ser.in_waiting:
            #print('serial in waiting')

            echoStr = str(ser.readline().decode()).strip(' ').strip('\n')
            #print(str(echoStr))
            Receiver = echoStr[0]
            if_STAGE_changed = echoStr[1]
            STAGE_changed = echoStr[2]
            if_STATE_changed = echoStr[3]
            STATE_changed = echoStr[4]
            if_Ultrasensor = echoStr[5]
            Ultrasensor_A = echoStr[6]
            Ultrasensor_B = echoStr[7]
            Ultrasensor_C = echoStr[8]
            Ultrasensor_D = echoStr[9]
            

            if Receiver=='P': # Arduino -> Python 
                 print('From arduino:', echoStr)
                 if if_STAGE_changed == '1': # button pressed, STAGE changed
                    #print("Change stage to:",STAGE_changed)
                    STAGE = STAGE_changed
                    STATE = 0
                 if if_STATE_changed == '1': # STATE changed
                    #print("Change state to:",STATE_changed)
                    STATE = STATE_changed

            if Receiver=='D': # Arduino debug messages
                print("\n-----")
                print("From debug:",echoStr[2:])
                print("-----\n")

except KeyboardInterrupt:
    ser.close()
    print('bye！')






