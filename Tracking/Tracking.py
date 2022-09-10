from telnetlib import ECHO
import serial
import time
import sys

TRACK_pwm_deflaut = 60
COM_PORT = 'COM5'
ser = serial.Serial(COM_PORT, 9600)
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

def write_serial(receiver='A',stage=0,state=0,pwm_L=0,pwm_R=0,fCam=0,sCam=0,stepper=0,pump=0):
    Py_input = str(receiver) + str(stage) + str(state) + Num2Str(pwm_L) + Num2Str(pwm_R)
    Py_input += str(fCam) + str(sCam) + str(stepper) + str(pump) + str("e")
    try:
        if len(Py_input) == 14:
            print("From py:",Py_input)
            ser.write(str.encode(Py_input))
    except:
        print("\n\nwrite serial error\n\n")


def get_TRACK_pwm(LF,LB,RF,RB):
    
    delta=0
    print("------\nLF:",LF," RF:",RF,"\nLB:",LB," RB:",RB,"\n------")

    """ If 'a' occurs on the left side """
    if LF=='a' and LB=='a':
        delta=20
    elif LF=='a' and LB=='b':
        delta=40
    elif LF=='b' and LB=='a':
        delta=-10
    elif LF=='a' and LB=='c':
        delta=60
    elif LF=='c' and LB=='a':
        delta=-30
    elif LF=='a' and LB=='d':
        delta=20
    elif LF=='d' and LB=='a':
        delta=20

    """ If 'a' occurs on the right side """
    if RF=='a' and RB=='a':
        delta=-20
    elif RF=='a' and RB=='b':
        delta=-40
    elif RF=='b' and RB=='a':
        delta=10
    elif RF=='a' and RB=='c':
        delta=-60
    elif RF=='c' and RB=='a':
        delta=30
    elif RF=='a' and RB=='d':
        delta=-20
    elif RF=='d' and RB=='a':
        delta=-20
    
    L=TRACK_pwm_deflaut+delta
    R=TRACK_pwm_deflaut-delta
    return L,R

try:
    while True:

        pwmL,pwmR = get_TRACK_pwm(Ultrasensor_A,Ultrasensor_B,Ultrasensor_C,Ultrasensor_D)
        print("\n\npwmL:",pwmL,"\npwmR",pwmR)
        write_serial('A',1,0,pwmL,pwmR)
        time.sleep(0.5)
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
                    

            if Receiver=='D': # Arduino debug messages
                print("\n-----")
                print("From debug:",echoStr[2:])
                print("-----\n")

except KeyboardInterrupt:
    ser.close()
    print('bye！')