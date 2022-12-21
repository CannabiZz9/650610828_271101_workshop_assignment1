#This code demonstrate how to show the video capture
import cv2
 
cap = cv2.VideoCapture(0)
 
while True:
    success, img = cap.read()
    cv2.imshow("Image", img)
    cv2.waitKey(1)

#Closeing all open windows
#cv2.destroyAllWindows()