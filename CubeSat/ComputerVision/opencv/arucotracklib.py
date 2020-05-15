import numpy as np
import cv2
import cv2.aruco as aruco
import sys, time, math

class ArucoSingleTracker():
    def __init__(self,
                id_to_find,
                marker_size,
                camera_matrix,
                camera_distortion,
                camera_size=[640,480],
                show_video=False
                ):
        
        
        self.id_to_find     = id_to_find
        self.marker_size    = marker_size
        self._show_video    = show_video
        
        self._camera_matrix = camera_matrix
        self._camera_distortion = camera_distortion
        
        self.is_detected    = False
        self._kill          = False
        
        #--- 180 deg rotation matrix around the x axis
        self._R_flip      = np.zeros((3,3), dtype=np.float32)
        self._R_flip[0,0] = 1.0
        self._R_flip[1,1] =-1.0
        self._R_flip[2,2] =-1.0

        #--- Define the aruco dictionary
        self._aruco_dict  = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
        self._parameters  = aruco.DetectorParameters_create()


        #--- Capture the videocamera (this may also be a video or a picture)
        #imgFlip=cv2.flip(frame,-1)

        self._cap = cv2.VideoCapture(0)
        #-- Set the camera size as the one it was calibrated with
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_size[0])
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_size[1])

        #-- Font for the text in the image
        self.font = cv2.FONT_HERSHEY_PLAIN

        self._t_read      = time.time()
        self._t_detect    = self._t_read
        self.fps_read    = 0.0
        self.fps_detect  = 0.0 


        
    def stop(self):
        self._kill = True
    

    # Finds aruco marker in camera sight (True/False)
    # Computes distances (x,y,z)
    # X : left/ right of camera
    # Y  : up/down from camera
    # Z : distance from camera 
    # Returns(boolean,intX,intY,intZ)
    def track(self, loop=True, verbose=False, show_video=True):
        
        self._kill = False
        if show_video is None: show_video = self._show_video
        
        marker_found = False
        x = y = z = 0
        
        while not self._kill:
            
            #-- Read the camera frame
            ret, frame = self._cap.read()
            # frame = cv2.flip(frame,0)
            # ret = cv2.flip(ret,0)
            
            #-- Convert in gray scale
            gray    = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #-- remember, OpenCV stores color images in Blue, Green, Red

            #-- Find all the aruco markers in the image
            corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=self._aruco_dict, 
                            parameters=self._parameters,
                            cameraMatrix=self._camera_matrix, 
                            distCoeff=self._camera_distortion)
                            
            if not ids is None and self.id_to_find in ids[0]:
                marker_found = True
                #-- ret = [rvec, tvec, ?]
                #-- array of rotation and position of each marker in camera frame
                #-- rvec = [[rvec_1], [rvec_2], ...]    attitude of the marker respect to camera frame
                #-- tvec = [[tvec_1], [tvec_2], ...]    position of the marker in camera frame
                ret = aruco.estimatePoseSingleMarkers(corners, self.marker_size, self._camera_matrix, self._camera_distortion)

                #-- Unpack the output, get only the first
                rvec, tvec = ret[0][0,0,:], ret[1][0,0,:]
                
                x = tvec[0]
                y = tvec[1]
                z = tvec[2]

                #-- Draw the detected marker and put a reference frame over it
                aruco.drawDetectedMarkers(frame, corners)
                aruco.drawAxis(frame, self._camera_matrix, self._camera_distortion, rvec, tvec, 10)

                #-- Obtain the rotation matrix tag->camera
                # R_ct    = np.matrix(cv2.Rodrigues(rvec)[0])
                # R_tc    = R_ct.T

                #-- Get the attitude in terms of euler 321 (Needs to be flipped first)

            

                #-- Now get Position and attitude f the camera respect to the marker
                # pos_camera = -R_tc*np.matrix(tvec).T
                # print( "Camera X = %4.0f  Y = %4.0f  Z = %4.0f ",(pos_camera[0], pos_camera[1], pos_camera[2]))
                if verbose: 
                    # print ("Marker X = %4.0f  Y = %4.0f  Z = %4.0f  - fps = %4.0f"%(tvec[0], tvec[1], tvec[2],self.fps_detect))
                    return(marker_found, x, y, z)

                if show_video:
                    font = cv2.FONT_HERSHEY_PLAIN


                    #-- Print the tag position in camera frame
                    str_position = "MARKER Position x=%4.0f  y=%4.0f  z=%4.0f"%(tvec[0], tvec[1], tvec[2])
                    cv2.putText(frame, str_position, (0, 100), font, 1, (0, 255, 0), 2, cv2.LINE_AA)        
                    
      

                    # str_position = "CAMERA Position x=%4.0f  y=%4.0f  z=%4.0f"%(pos_camera[0], pos_camera[1], pos_camera[2])
                    # cv2.putText(frame, str_position, (0, 200), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

              

            else:
                if verbose: 
                    print ("Nothing detected - fps = %.0f"%self.fps_read)
            

            if show_video:
                #--- Display the frame
                frame = cv2.flip(frame,0)
                cv2.imshow('frame', frame)

                #--- use 'q' to quit
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self._cap.release()
                    cv2.destroyAllWindows()
                    break
            
            if not loop: 
                return(marker_found, x, y, z)
            

# for testing purposes only 
if __name__ == "__main__":

    #--- Define Tag
    id_to_find  = 24
    marker_size  = 10 #- [cm]

    #--- Get the camera calibration path
    calib_path  = ""
    camera_matrix   = np.loadtxt(calib_path+'cameraMatrix_raspi.txt', delimiter=',')
    camera_distortion   = np.loadtxt(calib_path+'cameraDistortion_raspi.txt', delimiter=',')                                      
    aruco_tracker = ArucoSingleTracker(id_to_find=24, marker_size=10, show_video=False, camera_matrix=camera_matrix, camera_distortion=camera_distortion)
   
    # aruco_tracker.track(verbose=False)
    print(aruco_tracker.track(verbose=True))
    