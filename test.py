
import cv2
import numpy

Acquiring images from camera #
# Parameter is 0, which means open notebook built-in camera, video file parameter is the path to open the video
cap = cv2.VideoCapture(0)

while True:
    # get a frame
    # Capture.read () reads the video frame by frame
    # Ret, frame return value capture.read () method
    # Ret which is a Boolean value that, if the reading frame is correct, return True; if the file is read until the end, returns False.
    # Frame is each frame image is a three dimensional matrix
    ret, frame = cap.read()
    # show a frame
    cv2.imshow("capture", frame)
    # WaitKey () represents waiting for keyboard input
    #Parameter # 1, represents a 1ms delay is switched to the next frame of video in terms of
    # 0 parameters, to display only the current frame image, which is equivalent to pause video
    # Parameter is too large, due to excessive delay and Caton
    # asc = cv2.waitKey(1)
    #ASCII code # asc keyboard input, esc ASCII code corresponding to the key is 27
    # ASCII # value it a character (a string of length 1) as a parameter and returns the corresponding
    # asc = cv2.waitKey(1)
    # # print asc
    if asc == ord('q'):
        break

# Release camera
cap.release()
Close all windows image #
cv2.destroyAllWindows()