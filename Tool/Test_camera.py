import cv2
import numpy as np

cap = cv2.VideoCapture(0) #w:640 h:480


def find_lane(frame):
    
    img = frame
    poly_h, poly_w, L = 280, 160, 240
    """ frame mask """
    # create a zero array
    trapezoid_stencil = np.zeros_like(img[:,:,0])

    polygon = np.array([[0,480], [320-poly_w,480-poly_h], [320+poly_w,480-poly_h], [640,480]])

    # fill polygon with gray
    cv2.fillConvexPoly(trapezoid_stencil, polygon, 100)
    #cv2.imshow("gray trapezoid",trapezoid_stencil)

    trapezoid_view = cv2.bitwise_and(img,img,mask=trapezoid_stencil)
    #cv2.imshow("trapezoid view img",trapezoid_view)

    """ mark image """
    marked_img = img.copy()
    marked_img = cv2.cvtColor(marked_img,cv2.COLOR_BGR2HSV)

    cv2.polylines(marked_img,pts=[polygon],isClosed=True,color=(30,120,225),thickness=5) # draw polygon on marked img

    for scale in [(80,-5),(70,15),(60,48),(50,80),(40,125),(30,190),(20,270)]:  # mark each scale
        ycoord = 480-poly_h+scale[1]
        cv2.line(marked_img, (160, ycoord), (480, ycoord), (177, 80, 0), 4)
        cv2.putText(marked_img, str(scale[0]), (300,ycoord+5), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,0), 2, cv2.LINE_AA) 
        
    marked_img = cv2.cvtColor(marked_img,cv2.COLOR_HSV2BGR)
    
    return marked_img
    

while(True):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    Front_camera = find_lane(frame)
    
    """ find lane """
    #cv2.imshow("Front camera",Front_camera)
    
    
    """ fruit """
    x = 180
    y = 85
    w = 130
    h = 85

    polygon = np.array([[x,y], [x,y+h], [x+w,y+h], [x+w,y]])
    cv2.polylines(frame,pts=[polygon],isClosed=True,color=(20,180,225),thickness=3)

    """ box """
    x = 335
    y = 160
    w = 150
    h = 215
    polygon = np.array([[x,y], [x,y+h], [x+w,y+h], [x+w,y]])
    cv2.polylines(frame,pts=[polygon],isClosed=True,color=(60,120,225),thickness=3)
    
    """ carrot """
    x = 240
    y = 100
    w = 70
    h = 90
    polygon = np.array([[x,y], [x,y+h], [x+w,y+h], [x+w,y]])
    cv2.polylines(frame,pts=[polygon],isClosed=True,color=(180,70,25),thickness=3)
        
    #cv2.imshow('Side camera', frame)
    
    view = cv2.hconcat([Front_camera,frame])
    
    cv2.imshow('camera views', view)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
