
#!Hand Tracking Module(Which Can be used to Create Project,Reuse the Functionality.

import cv2
import mediapipe as mp
import time,math

class HandTracking():
    def __init__(self,
                 static_image_mode=False,
                 max_num_hands=2,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):

            self.mpHands=mp.solutions.hands
            self.hands=self.mpHands.Hands(static_image_mode=static_image_mode,max_num_hands=max_num_hands,min_detection_confidence=min_detection_confidence,min_tracking_confidence=min_tracking_confidence)

            self.mpdraw=mp.solutions.drawing_utils

            
    def FindHands(self,img,draw=True):
          imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

          self.result=self.hands.process(imgRGB)

          if self.result.multi_hand_landmarks is not None:
                for handlm in self.result.multi_hand_landmarks:
                      if draw:
                        self.mpdraw.draw_landmarks(img,handlm,self.mpHands.HAND_CONNECTIONS)
          return img
    
    
    def FindPos(self,img,Hand_no=0,draw=True):
          self.lmlist=[]
          
          if self.result.multi_hand_landmarks is not None:
                    handlm=self.result.multi_hand_landmarks[Hand_no]
            #    for handlm in self.result.multi_hand_landmarks:
                    for id,lm in enumerate(handlm.landmark):
                         
                         h,w,c=img.shape
                         cx,cy=int(lm.x*w),int(lm.y*h)

                         self.lmlist.append([id,cx,cy])

                         if draw:
                              cv2.circle(img,(cx,cy),25,(0,255,0),2)
                            #   cv2.circle(img,(cx,cy),25,(0,255,0),cv2.FILLED)
          
          return self.lmlist
    def FindPosition(self,img,HandNum=0,draw=True):
         lmList=[]
         xList = []
         yList = []
         bbox = []

         if self.result.multi_hand_landmarks is not None:
             myHand=self.result.multi_hand_landmarks[HandNum]
             for id,lm in enumerate(myHand.landmark):

                 h,w,c=img.shape
                 cx,cy= int(lm.x*w),int(lm.y*h)
                 xList.append(cx)
                 yList.append(cy)

                 #print(id,cx,cy)
                 lmList.append([id,cx,cy])
                 #if(id==0):
                 if draw:
                    cv2.circle(img,(cx,cy),25,(0,255,0),cv2.FILLED)
         if len(xList)!=0:
            xmin, xmax = min(xList), max(xList)
         else:
            xmin,xmax=0,0
         if len(yList)!=0:
            ymin, ymax = min(yList), max(yList)
         else:
            ymin,ymax=0,0

         if draw:
          cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
        (0, 255, 0), 2)

         return lmList,bbox

    def Fingersup(self,lmList):
       TipId=[4,8,12,16,20]
       fingers=[]
       if(lmList[TipId[0]][1]>lmList[TipId[0]-1][1]):
                 fingers.append(1)
       else:
                fingers.append(0)
       for id in range(1,5):
            if len(lmList)>=TipId[id] and lmList[TipId[id]][2] < lmList[TipId[id]-2][2]:
                 fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
       totalFingers=fingers.count(1)

       return fingers,totalFingers
    
    
    def FindDistance(self,lmList,p1,p2,img,draw=True,r=15,t=3):
       x1,y1=lmList[p1][1:]
       x2,y2=lmList[p2][1:]

       cx,cy=(x1+x2)//2,(y1+y2)//2

       if draw:
           cv2.line(img,(x1,y1),(x2,y2),(255,0,255),t)
           cv2.circle(img,(x1,y1),r,(255,0,255),cv2.FILLED)
           cv2.circle(img,(x2,y2),r,(255,0,255),cv2.FILLED)
           cv2.circle(img,(cx,cy),r,(0,0,255),cv2.FILLED)
       length=math.hypot(x2-x1,y2-y1)
       print("Distance")
       return length,img,{x1,y1,x2,y2,cx,cy}

#?Dummy Code To Test
def main():
    pTime,cTime=0,0

    cap=cv2.VideoCapture(0)

    detector=HandTracking()

    while True:
         success,img=cap.read()

         img=detector.FindHands(img)

         lmlist=detector.FindPos(img)

         cTime=time.time()
         fps=1/(cTime-pTime)
         pTime=cTime

         cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),3)
         cv2.imshow("Live",img)
         cv2.waitKey(1)












if __name__=="__main__":
     main()
