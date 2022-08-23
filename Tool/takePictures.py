import cv2

camera_port = 0

path1 = "C:\\Users\\BERLIN CHEN\\Desktop\\2021FR\\Photos\\box"
path2 = ".jpg"

cap = cv2.VideoCapture(camera_port) #w:640 h:480 for both notebook and camera
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#cap.set(cv2.CAP_PROP_BRIGHTNESS,5)

count = 1
while True:
  ret, frame = cap.read()
  cv2.imshow('frame', frame)
  path = path1 + str(count) + path2
  if cv2.waitKey(1) & 0xFF == ord('q'):
    cv2.imwrite(path, frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    cv2.imshow('picture captured', frame)
    count += 1
  

cv2.waitKey(0)
cap.release()

cv2.destroyAllWindows()


