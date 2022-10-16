import cv2
import numpy as np
import imutils
import math

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


def color_sign_recog(frame):
    area_threshold = 50000
    font = cv2.FONT_HERSHEY_PLAIN

    yellow_lower = np.array([23,59,90])   
    yellow_upper = np.array([28,255,255])  

    red_lower1 = np.array([0,43,70])   
    red_upper1 = np.array([10,255,255]) 
    red_lower2 = np.array([170,43,50])  
    red_upper2 = np.array([180,255,255])  

    blue_lower = np.array([100,43,70])
    blue_upper = np.array([140,255,255])

    black_lower = np.array([0,0,0])
    black_upper = np.array([255,255,70])

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (15, 15), 0)
    hsv = hsv[110:,0:]

    #yellow
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper) 
    yellow_mask = cv2.erode(yellow_mask, None, iterations=2)
    yellow_mask = cv2.dilate(yellow_mask, None, iterations=2)
    yellow_contours, yellow_hierarchy = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(yellow_contours) > 0:
        yellow_cnt = max(yellow_contours, key=cv2.contourArea)
        yellow_output = cv2.bitwise_and(hsv, hsv, mask = yellow_mask) 

        # cv2.drawContours(yellow_output, yellow_cnt, -1, (255, 255, 255), 3)
        # cv2.putText(yellow_output, str(cv2.contourArea(yellow_cnt)), (10, 200), font, 4, (0, 255, 255), 2, cv2.LINE_AA)
        # cv2.imshow('yellow', yellow_output)

        if cv2.contourArea(yellow_cnt) > area_threshold:
            return 'yellow'
    
    #red
    red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1) 
    red_mask1 = cv2.erode(red_mask1, None, iterations=2)
    red_mask1 = cv2.dilate(red_mask1, None, iterations=2)

    red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2) 
    red_mask2 = cv2.erode(red_mask2, None, iterations=2)
    red_mask2 = cv2.dilate(red_mask2, None, iterations=2)

    red_mask = cv2.bitwise_or(red_mask1, red_mask2)
    red_contours, red_hierarchy= cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(red_contours) > 0:
        red_cnt = max(red_contours, key=cv2.contourArea)
        red_output = cv2.bitwise_and(hsv, hsv, mask = red_mask)

        # cv2.drawContours(red_output, red_cnt, -1, (255, 255, 255), 3)
        # cv2.putText(red_output, str(cv2.contourArea(red_cnt)), (10, 200), font, 4, (0, 255, 255), 2, cv2.LINE_AA)
        # cv2.imshow('red', red_output)

        if cv2.contourArea(red_cnt) > area_threshold:
            return 'red'
    
    # blue
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper) 
    blue_mask = cv2.erode(blue_mask, None, iterations=2)
    blue_mask = cv2.dilate(blue_mask, None, iterations=2)
    blue_contours, blue_hierarchy= cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(blue_contours) > 0:
        blue_cnt = max(blue_contours, key=cv2.contourArea)
        blue_output = cv2.bitwise_and(hsv, hsv, mask = blue_mask)

        # cv2.drawContours(blue_output, blue_cnt, -1, (255, 255, 255), 3)
        # cv2.putText(blue_output, str(cv2.contourArea(blue_cnt)), (10, 200), font, 4, (0, 255, 255), 2, cv2.LINE_AA)
        # cv2.imshow('blue', blue_output)

        if cv2.contourArea(blue_cnt) > area_threshold:
            return 'blue'

    black_mask = cv2.inRange(hsv, black_lower, black_upper) 
    black_mask = cv2.erode(black_mask, None, iterations=2)
    black_mask = cv2.dilate(black_mask, None, iterations=2)
    black_contours, black_hierarchy= cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(black_contours) > 0:
        black_cnt = max(black_contours, key=cv2.contourArea)
        black_output = cv2.bitwise_and(hsv, hsv, mask = black_mask)
        # cv2.drawContours(black_output, black_cnt, -1, (255, 255, 255), 3)
        # cv2.putText(black_output, str(cv2.contourArea(black_cnt)), (10, 200), font, 4, (0, 255, 255), 2, cv2.LINE_AA)
        # cv2.line(black_output, (0, 110), (600, 110), (255, 255, 255))
        # cv2.imshow('black', black_output)

        if cv2.contourArea(black_cnt) > area_threshold:
            return 'black' 
    
    return 'null'
def take_shower(img):
    red1_lower = np.array([0,90,0])
    red1_upper = np.array([30,255,255])
    red2_lower = np.array([170,41,0])
    red2_upper = np.array([180,255,255])
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red_output1 = cv2.inRange(hsv, red1_lower, red1_upper)
    red_output2 = cv2.inRange(hsv, red2_lower, red2_upper)
    # hsv = cv2.GaussianBlur(hsv, (9,9), 0)
    red_mask = cv2.bitwise_or(red_output1, red_output2)
    red_mask = cv2.bitwise_and(img, img, mask=red_mask)
    red_mask = cv2.dilate(red_mask, None, iterations=18)
    red_mask = cv2.erode(red_mask, None, iterations=16)
    blur = cv2.GaussianBlur(red_mask,(3,3),0)
    thresh = cv2.Canny(blur, 30, 80)
    c = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

    lines = cv2.HoughLinesP(thresh, 1, math.pi/180, 120, 30, 5, 60)
    max_x1 = 0
    max_x2 = 0
    min_y1 = img.shape[1]
    max_y2 = 0
    try:
        for line in lines:
            for x1,y1,x2,y2 in line:
                if x1 > max_x1:
                    max_x1 = x1
                if x2 > max_x2:
                    max_x2 = x2
                if y1 < min_y1:
                    min_y1 = y1
                if y2 > max_y2:
                    max_y2 = y2
                # cv2.line(c, (x1,y1),(x2,y2),(255,255,0),10)
    except:
        print("no line")
    cv2.line(img, (max_x1,min_y1),(max_x2,max_y2),(0,255,0),15)

    # contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    # contours = imutils.grab_contours(contours)
    # contours = sorted(contours, key = cv2.contourArea, reverse=True)[:1]

    # for contour in contours:
    #     area = cv2.contourArea(contour)
    #     color = (0,255,0)
    #     if(area > 300):
    #         x, y, w, h = cv2.boundingRect(contour)
    #         img = cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
    #         img = cv2.putText(img, "red", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0))
                
    return max_x1, min_y1, max_x2, max_y2

# cap = cv2.VideoCapture(1)
# SIGN_COLOR = 'red'
# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()
# while True:
#     ret, img = cap.read()
#     if not ret:
#         print("Cannot receive frame")
#         break
    
#     max_x1, min_y1, max_x2, max_y2 = take_shower(img)
#     print("maxx1:",max_x1,"maxx2:",max_x2)
#     if max_x2 < 500 and max_x2 > 470 and SIGN_COLOR == 'red':
#         print("reach red!!")
#         STATE = 'W'
#         break
#     elif max_x2 < 500 and max_x2 > 470 and SIGN_COLOR == 'yellow':
#         print("reach yellow!!")
#         STATE = 'W'
#         break
#     elif max_x2 < 220 and max_x2 > 200 and SIGN_COLOR == 'blue':
#         print("reach blue!!")
#         STATE = 'W'
#         break
#     elif max_x2 < 220 and max_x2 > 200 and SIGN_COLOR == 'black':
#         print("reach black!!")
#         STATE = 'W'
#         break

#     cv2.imshow('result', img)
#     if cv2.waitKey(1) == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()
