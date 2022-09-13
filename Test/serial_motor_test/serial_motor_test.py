from telnetlib import ECHO
import serial
import time
import sys

TRACK_pwm_deflaut = 60
COM_PORT = 'COM7'
ser = serial.Serial(COM_PORT, 9600)

Ultrasensor_A,Ultrasensor_B,Ultrasensor_C,Ultrasensor_D = 'z','z','z','z'

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




pwmL = 60
pwmR = 60

try:    
    while True:
        print("\n\npwmL:",pwmL,"\npwmR",pwmR)
        write_serial('A',1,0,pwmL,pwmR)
        time.sleep(0.5)
        
            

except KeyboardInterrupt:
    ser.close()
    print('bye！')