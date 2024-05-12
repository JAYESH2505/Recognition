
#?Importing Library
import mediapipe as mp
import cv2
import time,math
import streamlit as st
import numpy as np
import autopy


#?Importing Module
from Modules import HandTracking as HT
from Modules import PoseEstimation as PE
from Modules import FaceDetection as FD

############
wCam,hCam=1080,1080
############

def main():
    
    st.title("Landmark Recognition")


    st.sidebar.title("Select The Recognition Type")
    
    option = st.sidebar.selectbox(
    'Select an option',
    ('Volume Control', 'Virtual Paint', 'Virtual Mouse','AI Personal Trainer')
)

    st.session_state.Continue=st.sidebar.button("Continue")

    if st.session_state.Continue:
        st.session_state.Continue=False       
        if option=="Volume Control":
            Run_app1()
        elif option=="Virtual Paint":
            Run_app2()
        elif option=="Virtual Mouse":
            Run_app3()
        elif option=="AI Personal Trainer":
            Run_app4()


def Run_app1():

    #? DISPLAYING
    st.write(f"<span style='font-size: 24px;'>Volume Control <b></b></span>", unsafe_allow_html=True)

    #? Creating Detector Object
    detector=HT.HandTracking(min_detection_confidence=0.75,min_tracking_confidence=0.75)
    face=FD.FaceEstimation()

    #? Code-------------->
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    # volume.GetMute()
    # volume.GetMasterVolumeLevel()
    volRange=(volume.GetVolumeRange())
    #Range -45--0
    # volume.SetMasterVolumeLevel(0.0, None)
    #? --------------------->

    #?Variable
    minvol=volRange[0]
    maxvol=volRange[1]

    vol,volBar,volPer=0,400,0


    #? Create An Empty space for the video Frame
    video_frame=st.empty()
    video_frame.markdown(
    '<style> .css-1v9yl2r { width: 1080px !important; height: 1080px !important; } </style>'
    '<div></div>',
    unsafe_allow_html=True
)


    #? Create a Video Capture Object
    capture=cv2.VideoCapture(1) # capture=cv2.VideoCapture(0)
    capture.set(3,wCam)
    capture.set(4,hCam)

    while True:

        #? Read the Frame from the video Capture
        success,frame=capture.read()
        
        #? Flip for External Camera
        frame=cv2.flip(frame,1)

        if not success:
            break
        
        #? Perform Hand Tracking on the Frame

        frame=detector.FindHands(frame,draw=True)
        Result=detector.FindPos(frame,draw=False)

        

        if(len(Result)!=0):
            
            x1,y1=Result[4][1],Result[4][2]
            x2,y2=Result[8][1],Result[8][2]

            cx,cy=(x1+x2)//2,(y1+y2)//2

            cv2.circle(frame,(x1,y1),15,(255,0,255),cv2.FILLED)
            cv2.circle(frame,(x2,y2),15,(255,0,255),cv2.FILLED)
            # cv2.circle(frame,(cx,cy),15,(255,0,255),cv2.FILLED)
            cv2.line(frame,(x1,y1),(x2,y2),(255,0,255),3)


            length=math.hypot(x2-x1,y2-y1)

            #Note Length of Line
            var1,var2=40,400

            vol=np.interp(length,[var1,var2],[minvol,maxvol])
            volBar=np.interp(length,[var1,var2],[400,150])
            volPer=np.interp(length,[var1,var2],[0,100])

            volume.SetMasterVolumeLevel(vol, None)
            # if length<20:
            #     cv2.circle(frame,(cx,cy),15,(0,255,0),3)
        
        
        cv2.rectangle(frame,(52+20,150),(85+20,400),(0,255,0),3)
        cv2.rectangle(frame,(52+20,int(volBar)),(85+20,400),(0,255,0),cv2.FILLED)
        cv2.putText(frame,f"Volume {int(volPer)}" ,(20,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

        #? Display the frame with hand tracking overlay
        video_frame.image(frame, channels="BGR", use_column_width=True)

    
    capture.release()

def Run_app2():

    #? DISPLAYING
    st.write(f"<span style='font-size: 24px;'>Virtual Painter <b></b></span>", unsafe_allow_html=True)

    Picture=cv2.imread('C:\Coading\Python\Vision\Project\VirtualPainter.py\VirtualPainter.jpg')

    #? Creating Object.
    detector=HT.HandTracking(min_detection_confidence=0.75,min_tracking_confidence=0.75)
    face=FD.FaceEstimation()

    #? Create An Empty space for the video Frame
    video_frame=st.empty()
    video_frame.markdown(
    '<style> .css-1v9yl2r { width: 1280px !important; height: 720px !important; } </style>'
    '<div></div>',
    unsafe_allow_html=True)

    #? Creating Video Capturing Object
    cap=cv2.VideoCapture(1) # cap=cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)


    color=(0,0,255)
    brushThickness=5
    eraserThickness=50
    xp,yp=0,0


    imgCanvas=np.zeros((720,1280,3),np.uint8)

    while True:
        success,img=cap.read()

        #? FLip the Image
        img=cv2.flip(img,1)

        #? Find Hand Landmarks
        img=detector.FindHands(img,draw=True)
        lmlist=detector.FindPos(img,draw=True)


        if len(lmlist)!=0:
            #Index finger
            x1,y1=lmlist[8][1:]

            #Middle finger
            x2,y2=lmlist[12][1:]

            #Check Which finger are up
            fingers,totalfingers=detector.Fingersup(lmlist)
            # print(totalFingers)

            #If selection Mode-Two Fingers are up
            if fingers[1] and fingers[2]:
                xp,yp=0,0
                cv2.rectangle(img,(x1,y1-15),(x2,y2+15),color,cv2.FILLED)
                print("Selection Mode")

                #Checking for the clicks
                if y1<135:
                    if 250<x1<450:
                        print("Red")
                        color=(0,0,255)
                    elif 550<x1<750:
                        print("Green")
                        color=(0,255,0)
                    elif 800<x1<950:
                        print("Yellow")
                        color=(255,255,0)
                    elif 1050<x1<1200:
                        print("Eraser")
                        color=(0,0,0)


            #If Drawing Mode-Index Finger is up
            if fingers[1] and fingers[2]==False:
                cv2.circle(img,(x1,y1),15,color,cv2.FILLED)
                print("Drawing Mode")

                if xp==0 and yp==0:
                    xp,yp=x1,y1
                
                if color==(0,0,0):
                    cv2.line(img,(xp,yp),(x1,y1),color,eraserThickness)
                    cv2.line(imgCanvas,(xp,yp),(x1,y1),color,eraserThickness)
                else:
                    cv2.line(img,(xp,yp),(x1,y1),color,brushThickness)
                    cv2.line(imgCanvas,(xp,yp),(x1,y1),color,brushThickness)
                xp,yp=x1,y1
        
        imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
        _,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
        imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)

        img=cv2.bitwise_and(img,imgInv)
        img=cv2.bitwise_or(img,imgCanvas)


        #Setting they Header Image
        img[:1280][:135]=Picture

        #? Display the frame with hand tracking overlay
        video_frame.image(img, channels="BGR", use_column_width=True)
        
    cap.release()   



def Run_app3():
    #? DISPLAYING
    st.write(f"<span style='font-size: 24px;'>Virtual Mouse <b></b></span>", unsafe_allow_html=True)

    Picture=cv2.imread('C:\Coading\Python\Vision\Project\VirtualPainter.py\VirtualPainter.jpg')

    #? Creating Object.
    detector=HT.HandTracking(min_detection_confidence=0.75,min_tracking_confidence=0.75)
    face=FD.FaceEstimation()

    #? Create An Empty space for the video Frame
    video_frame=st.empty()
    video_frame.markdown(
    '<style> .css-1v9yl2r { width:420px !important; height: 420px !important; } </style>'
    '<div></div>',
    unsafe_allow_html=True)

    #? Creating Video Capturing Object
    wcam=480
    hcam=480
    smoothlen=5
    plocx,plocy=0,0
    clocx,clocy=0,0

    #? Creating Capture Object
    cap=cv2.VideoCapture(1)
    cap.set(3,wcam)
    cap.set(4,hcam)

    frameReduction=100

    wscreen,hscreen=autopy.screen.size()

    while True:

        success,img=cap.read()

        #? Flip the Image
        img=cv2.flip(img,1)

        img=detector.FindHands(img)
        lmList,bbox=detector.FindPosition(img,draw=False)

        cv2.rectangle(img,(frameReduction,frameReduction),(wcam-frameReduction,hcam-frameReduction),(255,0,255),2)
        if len(lmList)!=0:
            #Get the tip of the index and middle fingers
            x1,y1=lmList[8][1:]
            x2,y2=lmList[12][1:]

            
            #Check which finger are up
            fingers,totalFingers=detector.Fingersup(lmList=lmList)

            #Only Index Finger:Moving mods
            if fingers[1]==1 and fingers[2]==0:
                
                #Convert our coordinate
   
                x3=np.interp(x1,(frameReduction,wcam-frameReduction),(0,wscreen))
                y3=np.interp(y1,(frameReduction,hcam-frameReduction),(0,hscreen))
                
                #Smoothen Value
                clocx=plocx+(x3-plocx)/smoothlen
                clocy=plocy+(y3-plocy)/smoothlen


                #Move Mouse
                autopy.mouse.move(clocx,clocy)
                cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
                plocx=clocx
                plocy=clocy

            #Both Index and Middle Fingers are up:Clicking mods
            if fingers[1]==1 and fingers[2]==1 and totalFingers==2:

                #Distance Between fingers
                length,img,info=detector.FindDistance(lmList,8,12,img)
                # time.sleep(1)
                if length<40:
                    autopy.mouse.click()

        #? Display the frame with hand tracking overlay
        video_frame.image(img, channels="BGR", use_column_width=True)
        
    cap.release()  


def Run_app4():

    #? DISPLAYING
    st.write(f"<span style='font-size: 24px;'>AI Personal Trainer <b></b></span>", unsafe_allow_html=True)


    #? Creating Object.
    detector=PE.poseDetector()
    face=FD.FaceEstimation()

    #? Create An Empty space for the video Frame
    video_frame=st.empty()
    video_frame.markdown(
    '<style> .css-1v9yl2r { width:720px !important; height: 1280px !important; } </style>'
    '<div></div>',
    unsafe_allow_html=True)


    #? Variable
    count = 0
    dir = 0
    wcam,hcam=1280,720

    #? Creating Capture Object
    cap=cv2.VideoCapture(1)
    cap.set(3,wcam)
    cap.set(4,hcam)


    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read frame")
            break
        
        # Ensure the frame has dimensions greater than zero
        if img.size == 0:
            print("Empty frame")
            continue
        
        img = detector.findPose(img, False)
        lmList = detector.getPosition(img, False)

        if len(lmList) != 0:  
            
            angle = detector.findAngle(img, 11, 13, 15)

            per = np.interp(angle, (210, 310), (0, 100))
            bar = np.interp(angle, (220, 310), (650, 100))
            
            # Check for Dumbell Curl
            color = (255, 0, 255)
            if per == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (0, 0, 255)
                if dir == 1:
                    count += 0.5
                    dir = 0
            
            # Display results
            cv2.rectangle(img, (1100, 100), (1175, 658), (0, 255, 0), 3)
            cv2.rectangle(img, (1100, int(bar)), (1175, 658), color, cv2.FILLED)
            cv2.putText(img, str(int(per)), (1080, 70), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 4)
            
            cv2.putText(img,f'Count {int(count)}', (45, 670), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
        #? Display the frame with hand tracking overlay
        video_frame.image(img, channels="BGR", use_column_width=True)
        
    cap.release()  
if __name__=="__main__":
    main()
