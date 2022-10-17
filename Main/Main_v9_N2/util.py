import re
import cv2
import numpy as np
import imutils


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
    area_threshold = 30000
    font = cv2.FONT_HERSHEY_PLAIN

    """ 10/15 revised """
    yellow_lower = np.array([25,121,160])   
    yellow_upper = np.array([50,255,255])  

    red_lower1 = np.array([0,43,70])   
    red_upper1 = np.array([10,255,255]) 
    red_lower2 = np.array([170,43,50])  
    red_upper2 = np.array([180,255,255])  


    """ 10/15 revised """
    blue_lower = np.array([82,38,108])
    blue_upper = np.array([113,255,255])

    """ 10/15 revised """
    black_lower = np.array([15,0,0])
    black_upper = np.array([178,255,110])

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.medianBlur(hsv, 17, 0)
    #cv2.imshow("find sign",hsv)
    #hsv = hsv[10:,0:]

    #yellow
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper) 
    yellow_mask = cv2.erode(yellow_mask, None, iterations=2)
    yellow_mask = cv2.dilate(yellow_mask, None, iterations=2)
    yellow_contours, yellow_hierarchy = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(yellow_contours) > 0:
        yellow_cnt = max(yellow_contours, key=cv2.contourArea)
        yellow_output = cv2.bitwise_and(hsv, hsv, mask = yellow_mask) 

        cv2.drawContours(yellow_output, yellow_cnt, -1, (255, 255, 255), 3)
        cv2.putText(yellow_output, str(cv2.contourArea(yellow_cnt)), (10, 200), font, 4, (0, 255, 255), 2, cv2.LINE_AA)
        # cv2.imshow('yellow', yellow_output)

        if cv2.contourArea(yellow_cnt) > area_threshold:
            return 'yellow',yellow_output
    
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

        cv2.drawContours(red_output, red_cnt, -1, (255, 255, 255), 3)
        cv2.putText(red_output, str(cv2.contourArea(red_cnt)), (10, 200), font, 4, (0, 255, 255), 2, cv2.LINE_AA)
        # cv2.imshow('red', red_output)

        if cv2.contourArea(red_cnt) > area_threshold:
            return 'red',red_output
    
    # blue
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper) 
    blue_mask = cv2.erode(blue_mask, None, iterations=2)
    blue_mask = cv2.dilate(blue_mask, None, iterations=2)
    blue_contours, blue_hierarchy= cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(blue_contours) > 0:
        blue_cnt = max(blue_contours, key=cv2.contourArea)
        blue_output = cv2.bitwise_and(hsv, hsv, mask = blue_mask)

        cv2.drawContours(blue_output, blue_cnt, -1, (255, 255, 255), 3)
        cv2.putText(blue_output, str(cv2.contourArea(blue_cnt)), (10, 200), font, 4, (0, 255, 255), 2, cv2.LINE_AA)
        # cv2.imshow('blue', blue_output)

        if cv2.contourArea(blue_cnt) > area_threshold:
            return 'blue',blue_output

    black_mask = cv2.inRange(hsv, black_lower, black_upper) 
    black_mask = cv2.erode(black_mask, None, iterations=2)
    black_mask = cv2.dilate(black_mask, None, iterations=2)
    black_contours, black_hierarchy= cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(black_contours) > 0:
        black_cnt = max(black_contours, key=cv2.contourArea)
        black_output = cv2.bitwise_and(hsv, hsv, mask = black_mask)
        cv2.drawContours(black_output, black_cnt, -1, (255, 255, 255), 3)
        cv2.putText(black_output, str(cv2.contourArea(black_cnt)), (10, 200), font, 4, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.line(black_output, (0, 110), (600, 110), (255, 255, 255))
        #cv2.imshow('black', black_output)

        if cv2.contourArea(black_cnt) > area_threshold:
            return 'black',black_output 
    
    return 'null',hsv

def recognition(img, distance, shape): 
    
    #try:
        rectangle_passArea = 2618.6*(distance**2) - 4915.4*distance + 17458
        triangle_passArea = 1835.7*(distance**2) - 3994.3*distance + 12240
        circle_passArea = 3760.7*(distance**2) - 9059.3*distance + 22140

        color1 = ((0,100,140),(13,255,255))
        color2 = ((170,186,145),(180,255,255))
        lower1 = np.array(color1[0], dtype='uint8')
        upper1 = np.array(color1[1], dtype='uint8')
        lower2 = np.array(color2[0], dtype='uint8')
        upper2 = np.array(color2[1], dtype='uint8')
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv, (9,9), 0)
        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask = cv2.bitwise_or(mask1, mask2 )
        mask = cv2.bitwise_and(img, img, mask=mask)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        blur = cv2.GaussianBlur(mask,(9,9),0)
        thresh = cv2.Canny(blur, 60, 80)

        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key = cv2.contourArea, reverse=True)[:1]


        for cnt in cnts:
            approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
            #print(len(approx))
            
            if len(approx)==3 and (shape=="Tri_R" or shape=="Tri_L"):
                screenCnt = approx
                # print("tri area:",cv2.contourArea(cnt))
                M = cv2.moments(cnt)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                cv2.circle(img, center, 1, (0,0,0), 4)
                direction = [center[0]-approx[0][0][0], center[0]-approx[1][0][0], center[0]-approx[2][0][0]]
                if sum(i>0 for i in direction)==1 and shape=="Tri_L": 
                    cv2.drawContours(img,[screenCnt],-1,(0,255,0),2) #left triangle
                    #TODO: if distance less than X , turn to the back left side
                    # cv2.imshow("result",img)
                    if cv2.contourArea(cnt) > triangle_passArea:
                        return True, img

                if sum(i>0 for i in direction)==2 and shape=="Tri_R":
                    cv2.drawContours(img,[screenCnt],-1,(255,255,0),2) #right triangle
                    #TODO: if distance less than X , turn to the back right side
                    # cv2.imshow("result",img)
                    if cv2.contourArea(cnt) > triangle_passArea:
                        return True, img

            elif len(approx)==4 and shape=="Rec":
                # print("rec area:",cv2.contourArea(cnt))
                screenCnt = approx
                cv2.drawContours(img,[screenCnt],-1,(255,0,0),2) #rectangle
                #TODO: if distance less than X , turn to the right
                # cv2.imshow("result",img)
                if cv2.contourArea(cnt) > rectangle_passArea:
                        return True, img
                

            elif len(approx) > 7 and shape=="Cir":
                # print("cir area:",cv2.contourArea(cnt))
                screenCnt = approx
                cv2.drawContours(img,[screenCnt],-1,(0,255,255),2) #circle
                #TODO: if distance less than X , turn 180° around
                # cv2.imshow("result",img)
                if cv2.contourArea(cnt) > circle_passArea:
                        return True, img
                
        return False, img
    # except:
    #     return False, img

# def main():
#     cap = cv2.VideoCapture(2)
#     while(True):
#         ret, img = cap.read()
#         if not ret:
#             print("Cannot receive frame")
#             break
        
#         DRIFT, result = recognition(img,1,"Tri_L")
#         print(DRIFT)
#         cv2.imshow('result', result)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

# cap = cv2.VideoCapture(1)

# while True:
#     ret, frame = cap.read()
#     # cv2.imshow("frame",frame)
#     # cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U,0)
#     # print(cap.get(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U))
#     color, output = color_sign_recog(frame)
#     cv2.imshow("find sign",output)
#     if cv2.waitKey(1) == ord('Q'):
#         break
#     #print(color)  
    
# cv2.waitKey()
# cap.release()
# cv2.destroyAllWindows()
  