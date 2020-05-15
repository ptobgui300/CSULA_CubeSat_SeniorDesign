import numpy as np
import cv2
import cv2.aruco as aruco
import sys, time, math

class ArucoTracker():
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

    # def _rotationMatrixToEulerAngles(self,R):
    # # Calculates rotation matrix to euler angles
    # # The result is the same as MATLAB except the order
    # # of the euler angles ( x and z are swapped ).
    
    #     def isRotationMatrix(R):
    #         Rt = np.transpose(R)
    #         shouldBeIdentity = np.dot(Rt, R)
    #         I = np.identity(3, dtype=R.dtype)
    #         n = np.linalg.norm(I - shouldBeIdentity)
    #         return n < 1e-6        
    #     assert (isRotationMatrix(R))

    #     sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    #     singular = sy < 1e-6

    #     if not singular:
    #         x = math.atan2(R[2, 1], R[2, 2])
    #         y = math.atan2(-R[2, 0], sy)
    #         z = math.atan2(R[1, 0], R[0, 0])
    #     else:
    #         x = math.atan2(-R[1, 2], R[1, 1])
    #         y = math.atan2(-R[2, 0], sy)
    #         z = 0

    #     return np.array([x, y, z])

    def _update_fps_read(self):
        t           = time.time()
        self.fps_read    = 1.0/(t - self._t_read)
        self._t_read      = t
        
    def _update_fps_detect(self):
        t           = time.time()
        self.fps_detect  = 1.0/(t - self._t_detect)
        self._t_detect      = t    

    def stop(self):
        self._kill = True
    

    # Finds aruco marker in camera sight (True/False)
    # Computes distances (x,y,z)
    # X : left/ right of camera
    # Y  : up/down from camera
    # Z : distance from camera 
    # Returns(boolean,intX,intY,intZ)
    def track(self, loop=True, info=True, show_video=None):
        
        self._kill = False
        if show_video is None: show_video = self._show_video
        
        marker_found = False
        x = y = z = 0
        
        while not self._kill:
            
            #-- Read the camera frame
            ret, frame = self._cap.read()

            self._update_fps_read()
            
            #-- Convert in gray scale
            gray    = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #-- remember, OpenCV stores color images in Blue, Green, Red

            #-- Find all the aruco markers in the image
            corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=self._aruco_dict, 
                            parameters=self._parameters,
                            cameraMatrix=self._camera_matrix, 
                            distCoeff=self._camera_distortion)
                            
            if not ids is None and self.id_to_find in ids[0]:
                marker_found = True
                self._update_fps_detect()
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
                drawnmarker = aruco.drawDetectedMarkers(frame, corners)
                drawAxis   = aruco.drawAxis(frame, self._camera_matrix, self._camera_distortion, rvec, tvec, 10)

                #-- Obtain the rotation matrix tag->camera
                R_ct    = np.matrix(cv2.Rodrigues(rvec)[0])
                R_tc    = R_ct.T

                #-- Get the attitude in terms of euler 321 (Needs to be flipped first)
                # roll_marker, pitch_marker, yaw_marker = self._rotationMatrixToEulerAngles(self._R_flip*R_tc)

            

                #-- Now get Position and attitude f the camera respect to the marker
                pos_camera = -R_tc*np.matrix(tvec).T
                # print( "Camera X = %4.0f  Y = %4.0f  Z = %4.0f ",(pos_camera[0], pos_camera[1], pos_camera[2]))

               
                if info: 
                    print ("Marker X = %4.0f  Y = %4.0f  Z = %4.0f  - fps = %4.0f"%(tvec[0], tvec[1], tvec[2],self.fps_detect))
                    return(marker_found, x, y, z,str_attitude)

                if show_video:
                    font = cv2.FONT_HERSHEY_PLAIN


                    #-- Print the tag position in camera frame
                    str_position = "MARKER Position x=%4.0f  y=%4.0f  z=%4.0f"%(tvec[0], tvec[1], tvec[2])
                    cv2.putText(frame, str_position, (0, 100), font, 1, (0, 255, 0), 2, cv2.LINE_AA)        
                    
                    #-- Print the marker's attitude respect to camera frame
                    # str_attitude = "MARKER Attitude r=%4.0f  p=%4.0f  y=%4.0f"%(math.degrees(roll_marker),math.degrees(pitch_marker),
                    #                     math.degrees(yaw_marker))
                    # cv2.putText(frame, str_attitude, (0, 150), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

                    str_position = "CAMERA Position x=%4.0f  y=%4.0f  z=%4.0f"%(pos_camera[0], pos_camera[1], pos_camera[2])
                    cv2.putText(frame, str_position, (0, 200), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

                    #-- Get the attitude of the camera respect to the frame
                    # roll_camera, pitch_camera, yaw_camera = self._rotationMatrixToEulerAngles(self._R_flip*R_tc)

                    # str_attitude = "CAMERA Attitude r=%4.0f  p=%4.0f  y=%4.0f"%(math.degrees(roll_camera),math.degrees(pitch_camera),
                    #                     math.degrees(yaw_camera))
                    # cv2.putText(frame, str_attitude, (0, 250), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

            else:
                # if nothing found keep searching , 
                # uncomment line to  stop searching and return[false,0,0,0]
                if info: 
                    # print ("Marker X = 0,Y = 0 , Z =0 ,Nothing detected - fps = %.0f"%self.fps_read)


                    return(marker_found, x, y, z, )


            if show_video:
                #--- Display the frame
                cv2.imshow('frame', frame)

                #--- use 'q' to quit
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self._cap.release()
                    cv2.destroyAllWindows()
                    break
            
            if not loop: 
                return(marker_found, x, y, z)
            

if __name__ == "__main__":

    #--- Define Tag
    id_to_find  = 24
    marker_size  = 100 #- [cm]

    #--- Get the camera calibration path
    calib_path  = ""
    camera_matrix   = np.loadtxt(calib_path+'cameraMatrix_raspi.txt', delimiter=',')
    camera_distortion   = np.loadtxt(calib_path+'cameraDistortion_raspi.txt', delimiter=',')                                      
    aruco_tracker = ArucoTracker(id_to_find=24, marker_size=10, show_video=True, camera_matrix=camera_matrix, camera_distortion=camera_distortion)
    a = aruco_tracker.track(info=True)

while True :    
    print (a)
    
    


























