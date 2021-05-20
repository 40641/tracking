import cv2
import mediapipe as mp
import time
import rtde_control
import rtde_receive
import rtde_io
import math



class handDetector():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.8, trackCon=0.8):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
    


        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]



            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy =round(float(lm.x*w/1000), 3), round(float(lm.y*h/1000), 3)
                
                #print(id, cx, cy)
                # lmList.append([id, cx, cy])
                lmList.append([cx, cy])
                
                
                # if draw:
                #     cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

              
        return lmList


def main():

    Offset = 0.0001
    pTime = 0
    cTime = 0
    rtde_c = rtde_control.RTDEControlInterface("192.168.88.129")
    rtde__IO = rtde_io.RTDEIOInterface("192.168.88.129")
    rtde_r = rtde_receive.RTDEReceiveInterface("192.168.88.129")

    cap = cv2.VideoCapture(-1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 564)      #kamera felbontás, szélesség
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)     #kamera felbontás, magasság
    
    detector = handDetector()

    center = 0
    threshold = 0.05
        
    actual_tcp_pose = rtde_r.getActualTCPPose()
    while True:
        

        success, img = cap.read()
        img = detector.findHands(img)

        lmList = detector.findPosition(img)
        if len(lmList) != 0:
                       
            x_cord = lmList[0][0] - 0.320
            y_cord = lmList[0][1] *(-1) + 0.170

            x1_cord = lmList[4][0]
            y1_cord = lmList[4][1]

            x2_cord = lmList[8][0]
            y2_cord = lmList[8][1]

            lenght = round(math.sqrt((x2_cord-x1_cord)**2+(y2_cord-y1_cord)**2), 3)

            #rtde_c.moveL([float(x_cord), -0.500, float(y_cord) , 3.14, 0, 0], 1, 1)

            if lenght < 0.06:
                rtde__IO.setStandardDigitalOut(6, False)
                rtde__IO.setStandardDigitalOut(7, True)
                gripper = "close"
            else:
                rtde__IO.setStandardDigitalOut(7, False)
                rtde__IO.setStandardDigitalOut(6, True)
                gripper = "open"
#--------------------------------------------------------------------------------------------------------- 
            if x_cord >= center+threshold:
                actual_tcp_pose[0]=actual_tcp_pose[0]+Offset
                rtde_c.moveL([actual_tcp_pose[0], actual_tcp_pose[1], 0.400 , 3.14, 0, 0], 1, 1)
                #print("1")
#---------------------------------------------------------------------------------------------------------                 
            if y_cord >= center+threshold:
                actual_tcp_pose[1]=actual_tcp_pose[1]+Offset
                rtde_c.moveL([actual_tcp_pose[0], actual_tcp_pose[1], 0.400 , 3.14, 0, 0], 1, 1)
                #print("2")
  #---------------------------------------------------------------------------------------------------------          
            if y_cord <= center-threshold:
                actual_tcp_pose[1]=actual_tcp_pose[1]-Offset
                rtde_c.moveL([actual_tcp_pose[0], actual_tcp_pose[1], 0.400 , 3.14, 0, 0], 1, 1)
                #print("3")
  #--------------------------------------------------------------------------------------------------------- 
            if x_cord <= center-threshold:

                actual_tcp_pose[0]=actual_tcp_pose[0]-Offset
                rtde_c.moveL([actual_tcp_pose[0], actual_tcp_pose[1], 0.400 , 3.14, 0, 0], 1, 1)
                #print("4")           
  #--------------------------------------------------------------------------------------------------------- 
            

            print(f"robot_x_poz={actual_tcp_pose[0]}, robot_y_poz={actual_tcp_pose[1]}, kéz_x_kord={x_cord},kéz_y_kord={y_cord}, megfogó= {gripper}")
            
            #print(x_cord, y_cord)
            #print(lenght)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,30), cv2.FONT_HERSHEY_PLAIN,2, (0,0,255), 2)
               
        
        cv2.imshow("image", img)
        
        cv2.waitKey(1)
    
  
if __name__ == "__main__":
    main()
