import cv2
import mediapipe as mp
import time
import rtde_control



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
    pTime = 0
    cTime = 0
    #z= input("z magassag a tizedes vesszo az legyen pont (0.250-nél nagyobb):")
   # rtde_c = rtde_control.RTDEControlInterface("10.22.0.91")
   # rtde_r = rtde_receive.RTDEReceiveInterface("10.22.0.91")
   # 

    

    #rtde_c.moveL([0.108,-0.573, float(z), 0, 3.14, 0], 0.5, 0.3)

    cap = cv2.VideoCapture(-1)

         #kamera felbontás, magasság
    
  

    detector = handDetector()


    pose = ["balra", "jobbra", "fent", "lent"]
    
    while True:
        success, img = cap.read()
        img = detector.findHands(img)

        #actual_pose = rtde_r.getActualQ()
        
        
        
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
                       
            x_cord = round(lmList[0][0]-0.320, 3)
            z_cord = round((-1)*lmList[0][1]+0.240, 3)







            #rtde_c.moveL([float(x_cord),-0.500, float(z_cord) , 3.14, 0, 0], 0.5, 0.3)

            

            #rtde_c.moveL([float(x_cord),-0.500, float(z_cord) , 3.14, 0, 0], 0.5, 0.3)

            # time.sleep(0.015)


            #print(x_cord, z_cord)
            

        


        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,30), cv2.FONT_HERSHEY_PLAIN,2, (0,0,255), 2)
               
        
        cv2.imshow("image", img)
        
        cv2.waitKey(1)
    
  
if __name__ == "__main__":
    main()
