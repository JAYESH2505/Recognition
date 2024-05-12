
#! This is A Module for Face Estimation which helps us in creating Project And Work Easly.


#?Importing
import mediapipe as mp
import cv2
import time,math


class FaceEstimation():
    def __init__(self,Minimum_Detectionconfig=0.5) -> None:
        self.Minimum_Detectionconfig=Minimum_Detectionconfig


        self.myFaceDetection=mp.solutions.face_detection
        self.FaceDetection=self.myFaceDetection.FaceDetection(self.Minimum_Detectionconfig)
        self.myDraw=mp.solutions.drawing_utils


    def FindFace(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        Result=self.FaceDetection.process(imgRGB)

        Bounding_Box=[]

        if Result.detections:
            for id,detection in enumerate(Result.detections):
                if draw:
                    self.myDraw.draw_detection(img,detection)

            Bounding_box=detection.location_data.relative_bounding_box
            ih,iw,ic=img.shape
            Bounding=int(Bounding_box.xmin*iw),int(Bounding_box.ymin*ih),int(Bounding_box.width*iw),int(Bounding_box.height*ih)
            Bounding_Box.append([id,Bounding,detection.score])
            if draw:
                img=self.FancyBox(img,Bounding)
                 # cv2.rectangle(img,Bounding,(255,115,255),2)
                cv2.putText(img,f"Score {int(detection.score[0]*100)} %",(Bounding[0],Bounding[1]-20),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
            
        return img,Bounding
    #Create Fancy Box for image
    def FancyBox(self,img,bbox,l=30,t=10,rt=1):
        x,y,w,h=bbox
        x1,y1=x+w,y+h

        #Just Genral box.

        cv2.rectangle(img,(bbox),(255,255,255),rt)

        # Top Left
        cv2.line(img,(x,y),(x+l,y),(255,0,255),t)
        cv2.line(img,(x,y),(x,y+l),(255,0,255),t)

        # Top Right
        cv2.line(img,(x1,y),(x1-l,y),(255,0,255),t)
        cv2.line(img,(x1,y),(x1,y+l),(255,0,255),t)

        # Bottom Left
        cv2.line(img,(x,y1),(x+l,y1),(255,0,255),t)
        cv2.line(img,(x,y1),(x,y1-l),(255,0,255),t)

        # Top Left
        cv2.line(img,(x1,y1),(x1-l,y1),(255,0,255),t)
        cv2.line(img,(x1,y1),(x1,y1-l),(255,0,255),t)
        return img
    


def main():
    cap=cv2.VideoCapture(0)

    pTime,cTime=0,0

    detector=FaceEstimation(0.5)

    while True:
        success,img=cap.read()

        img,BBOX=detector.FindFace(img)
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime

        cv2.putText(img,str(int(fps)),(20,20),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
        cv2.imshow("Live",img)
        cv2.waitKey(1)



if __name__=="__main__":
    main()