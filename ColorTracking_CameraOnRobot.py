import cv2
import numpy as np
import time
import rtde_control

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)      #kamera felbontás, szélesség
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)     #kamera felbontás, magasság
cv2.namedWindow("Trackbars")
    

cv2.createTrackbar("L - H", "Trackbars", 170, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 55, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

cTime = 0
pTime = 0 

while True:
   
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    
    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    result = cv2.bitwise_and(frame, frame, mask=mask)


    color_track = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]


    if len(color_track)>0:
        blue_area = max(color_track, key=cv2.contourArea)
        (xg,yg,wg,hg) = cv2.boundingRect(blue_area)
        cv2.rectangle(frame,(xg,yg),(xg+wg, yg+hg),(0,255,0),2)    #téglalap kirajzolása


        centerOfCircle =((xg+xg+wg)//2, (yg+yg+hg)//2)
        Circle_x_cord = round(centerOfCircle[0] / 1000 , 3)      
        Circle_y_cord = round(centerOfCircle[1] /1000 , 3)  #Kör középpontja eltolva, kamerafelbontás módosítás esetén módosítani kell
        
        result_middle = cv2.circle(frame, centerOfCircle, radius=3, color=(0,255,0), thickness=(2))  #Téglalap középpontjának kirajzolása

        print(Circle_x_cord, Circle_y_cord)    #Tárgy középpontjának a koordinátáinak kiírása
        #time.sleep(0.15)



        #rtde_c = rtde_control.RTDEControlInterface("10.22.0.91")

        #rtde_c.moveL([float(Circle_y_cord*0.95),float(Circle_x_cord*1.02), 0.3, 3.14, 0, 0], 0.2, 0.2)
    

    #fps counter
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (10,30), cv2.FONT_HERSHEY_PLAIN,2, (0,0,255), 2)


    
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
   # cv2.imshow("result", result)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()