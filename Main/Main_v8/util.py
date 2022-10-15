import serial


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


