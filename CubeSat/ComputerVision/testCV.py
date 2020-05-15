from arucotrack import *
import time
import math

if __name__ == "__main__":

    #--- Define Tag
    id_to_find  = 24
    marker_size  = 10 #- [cm]

    #--- Get the camera calibration path
    calib_path  = ""
    camera_matrix   = np.loadtxt(calib_path+'cameraMatrix_raspi.txt', delimiter=',')
    camera_distortion   = np.loadtxt(calib_path+'cameraDistortion_raspi.txt', delimiter=',')                                      
    aruco_tracker = ArucoTracker(id_to_find=24, marker_size=10, show_video=False, camera_matrix=camera_matrix, camera_distortion=camera_distortion)

    print(aruco_tracker.track(info=True))

    time.sleep(5.0)
    print("Printed after 5.0 seconds.")    
    # print(aruco_tracker.track(info=True))
    # math.degrees(math.atan(1.18))



# Displacement
# Average velocity
