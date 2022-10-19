import serial
import numpy as np
import cv2
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
#     cap = cv2.VideoCapture(1)
#     while(True):
#         ret, img = cap.read()
#         if not ret:
#             print("Cannot receive frame")
#             break
        
#         DRIFT, result = recognition(img,1,"Tri_R")
#         print(DRIFT)
#         cv2.imshow('result', result)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()