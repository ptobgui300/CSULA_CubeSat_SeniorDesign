


# Note : flip camera for Raspberry pi  

import numpy as np
import cv2
import cv2.aruco as aruco
import sys, time, math

#--- Define Tag

class CubeArucoDetect :


    def detectMarker():
        id_to_find  = 24
        marker_size  = 10 #- [cm]



        #--- Get the camera calibration path
        calib_path  = ""
        camera_matrix   = np.loadtxt(calib_path+'cameraMatrix_raspi.txt', delimiter=',')
        camera_distortion   = np.loadtxt(calib_path+'cameraDistortion_raspi.txt', delimiter=',')



        #--- Define the aruco dictionary
        aruco_dict  = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
        parameters  = aruco.DetectorParameters_create()


        #--- Capture the videocamera (this may also be a video or a picture)
        cap = cv2.VideoCapture(0)
        #-- Set the camera size as the one it was calibrated with
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        #-- Font for the text in the image
        font = cv2.FONT_HERSHEY_PLAIN

        while True:

            #-- Read the camera frame
            ret, frame = cap.read()

            #-- Convert in gray scale
            gray    = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #-- remember, OpenCV stores color images in Blue, Green, Red

            #-- Find all the aruco markers in the image
            corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict, parameters=parameters,
                                    cameraMatrix=camera_matrix, distCoeff=camera_distortion)
            
            if ids is not None and ids[0] == id_to_find:
                #-- ret = [rvec, tvec, ?]
                #-- array of rotation and position of each marker in camera frame
                #-- rvec = [[rvec_1], [rvec_2], ...]    attitude of the marker respect to camera frame
                #-- tvec = [[tvec_1], [tvec_2], ...]    position of the marker in camera frame
                ret = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)

                #-- Unpack the output, get only the first

                #-- Draw the detected marker and put a reference frame over it
                aruco.drawDetectedMarkers(frame, corners)

                print("found / detected marker ! .. .  . .!")
                
                




            #--- Display the frame
            cv2.imshow('frame', frame)



            #--- use 'q' to quit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break






a = CubeArucoDetect.detectMarker()





















