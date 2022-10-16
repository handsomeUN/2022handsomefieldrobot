import cv2
import numpy as np

        
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

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    color = color_sign_recog(frame)
    if cv2.waitKey(1) == ord('Q'):
        break
    # print(color)  
cap.release()
cv2.destroyAllWindows()