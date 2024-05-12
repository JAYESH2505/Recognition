
#? This is a Module which is Created Using Mediapipe to Make Project and Work with it very Easily.


import cv2
import mediapipe as mp
import time,math

class poseDetector():

    def __init__(self,mode=False,upBody=False,smooth=True,detectionconf=True,trackingconf=True) -> None:
        self.mode=mode
        self.upBody=upBody
        self.smooth=smooth
        self.detectionconf=detectionconf
        self.trckingconf=trackingconf
        self.lmList=[]

        self.mpDraw=mp.solutions.drawing_utils
        self.mpPose=mp.solutions.pose
        self.pose=self.mpPose.Pose(self.mode,self.upBody,self.smooth,self.detectionconf,self.trckingconf)

    def findPose(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result=self.pose.process(imgRGB)
        if self.result.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.result.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img

    def getPosition(self,img,draw=True):
        self.lmList=[]
        if self.result.pose_landmarks:
            for id,lm in enumerate(self.result.pose_landmarks.landmark):
                h,w,c=img.shape
                # print(id,lm)
                # To obtain Pixel value
                cx,cy=int(lm.x*w),int(lm.y*h)
                self.lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)
        return self.lmList

    def findAngle(self,img,p1,p2,p3,draw=True)->None:
            x1,y1=self.lmList[p1][1:]
            x2,y2=self.lmList[p2][1:]
            x3,y3=self.lmList[p3][1:]

            #Calculate Angle
            angle=math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
            if angle<0:
                angle+=360
            # print(angle)

            if draw:
                cv2.line(img,(x1,y1),(x2,y2),(255,255,255),3)
                cv2.line(img,(x2,y2),(x3,y3),(255,255,255),3)
                cv2.circle(img,(x1,y1),10,(255,0,0),cv2.FILLED)
                cv2.circle(img,(x1,y1),15,(255,0,0),2)
                cv2.circle(img,(x2,y2),10,(255,0,0),cv2.FILLED)
                cv2.circle(img,(x2,y2),15,(255,0,0),2)
                cv2.circle(img,(x3,y3),10,(255,0,0),cv2.FILLED)
                cv2.circle(img,(x3,y3),15,(255,0,0),2)
                # cv2.putText(img,str(int(angle)),(x2-20,y2+50),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),4)

            return angle
    
def main():
    cap=cv2.VideoCapture(0)
    pTime=0
    detector=poseDetector()
    while True:
        sucess,img=cap.read()
        img=detector.findPose(img)
        lmList=detector.getPosition(img)

        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
    
        cv2.putText(img,str(int(fps)),(80,80),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),3)
        cv2.imshow("Image",img)
    
        cv2.waitKey(10)





if __name__=="__main__":
    main()