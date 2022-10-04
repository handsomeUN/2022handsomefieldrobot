from telnetlib import ECHO
import serial
import time
import sys

COM_PORT = 'COM6'
ser = serial.Serial(COM_PORT, 9600)

def Num2Str(num):
    if str(type(num)) == "<class 'int'>":
        cvt = str(num)
        if cvt[0] == '-':
            if len(cvt) ==3: #e.g. -50
                cvt = '-0' + str(int(-num/10))
            if len(cvt) ==4: #e.g. -200
                cvt = '-' + str(int(-num/10))
        else:    
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
            print("\nFrom py:",Py_input)
            ser.write(str.encode(Py_input))
    except:
        print("\n\nwrite serial error\n\n")




pwmL = 200
pwmR = 50

try:    
    #write_serial('A',1,0,pwmL,pwmR)
    # pwmL = input("pwm L:")
    # pwmR = input("pwm R:")
    while True:
        time.sleep(1)
        write_serial('A',1,0,pwmL,pwmR)
        time.sleep(0.2)
        
        while ser.in_waiting:
            #print('serial in waiting')
            echoStr = str(ser.readline().decode()).strip(' ').strip('\n')
            print(str(echoStr))
            #print("\n\npwmL:",pwmL,"\npwmR:",pwmR)
            time.sleep(0.2)
            

except :
    ser.close()
    print('bye！')