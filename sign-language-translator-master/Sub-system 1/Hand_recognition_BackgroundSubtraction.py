import cv2
import numpy as np
import imutils
import csv
import pandas as pd
#from scipy.spatial import ConvexHull

bg = None

def run_avg(image, aWeight):
    global bg
    # initialize the background
    if bg is None:
        bg = image.copy().astype("float")
        return

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(image, bg, aWeight)

def segment(image, threshold=25):
    global bg
    # find the absolute difference between background and current frame
    diff = cv2.absdiff(bg.astype("uint8"), image)

    # threshold the diff image so that we get the foreground
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    # get the contours in the thresholded image
    contours = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # FOR 4 DOTS AT EACH EXTREME POSITION
    contours = imutils.grab_contours(contours)

    # return None, if no contours detected
    if len(contours) == 0:
        return
    else:
                   
        # based on contour area, get the maximum contour which is the hand
        segmented = max(contours, key=cv2.contourArea)
        return (thresholded, segmented, contours)
    
if __name__ == "__main__":
    # initialize weight for running average
    aWeight = 0.5
    # get the reference to the webcam
    camera = cv2.VideoCapture(0)

    # region of interest (ROI) coordinates
    #small region
    top, right, bottom, left = 80, 400, 400, 590
    #top, right, bottom, left = 80, 0, 400, 190
    
    #full screen
    #top, right, bottom, left = 0, 0, 600, 800

    # initialize num of frames
    num_frames = 0

    # keep looping, until interrupted
    while(True):
        # get the current frame
        (grabbed, frame) = camera.read()
        
        # resize the frame
        frame = imutils.resize(frame, width=700)
       
        # flip the frame so that it is not the mirror view
        frame = cv2.flip(frame, 1)

        # clone the frame
        clone = frame.copy()

        # get the height and width of the frame
        (height, width) = frame.shape[:2]
        
        # get the ROI
        roi = frame[top:bottom, right:left]
        
        
  
        
        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # to get the background, keep looking till a threshold is reached
        # so that our running average model gets calibrated
        
        if num_frames < 30:
            run_avg(gray, aWeight)
        else:
                # segment the hand region
            hand = segment(gray)
           # cv2.imshow("hand", hand)
            
            # check whether hand region is segmented
            if hand is not None:
                # if yes, unpack the thresholded image and
                # segmented region
                (thresholded, segmented, contours) = hand
     
                cnts = len(contours)
                c = 0
                with open('cntrss.csv',mode='w') as csvfile:                
                    while c < cnts:
                        cntr = contours[c]
                        np_im = np.array(cntr)
                        hull = cv2.convexHull(cntr,returnPoints = False)
                        defects = cv2.convexityDefects(cntr,hull)
                        if defects is not None:
                            for i in range(defects.shape[0]):
                                s,e,f,d = defects[i,0]
                                start = tuple(cntr[s][0]+ (right,top))
                                end = tuple(cntr[e][0]+ (right,top))
                                far = tuple(cntr[f][0]+ (right,top))
                                M = cv2.moments(thresholded)
                                cx = int(M['m10']/M['m00']) + right
                                cy = int(M['m01']/M['m00']) + top
                                cv2.circle(clone,(cx,cy),3,[0,0,255],-1)
                                cv2.line(clone,start,end,[255,0,0],2)
                                cv2.circle(clone,far,6,[0,0,255],-1)
                                writer = csv.writer(csvfile, delimiter=',')
                                writer.writerow(start)
                                writer.writerow(end)
                                print (start,"/",end)
                                #print (d)
                        c=c+1
                       
                # draw the segmented region and display the frame
                cv2.drawContours(clone, [segmented + (right,top)], -1, (0, 255, 0),2)
                
                cv2.imshow("Thresholded", thresholded)
                
        # draw the segmented hand
        cv2.rectangle(clone, (left, top), (right, bottom), (0,0,0), 2)

        # increment the number of frames
        num_frames += 1

        # display the frame with segmented hand
        cv2.imshow("Video Feed", clone)
        
        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF
        
        #for reseting the frames to start from first frame again
        if keypress == ord("r"):
            num_frames = 0
      
        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
          
            break

# free up memory
camera.release()
cv2.destroyAllWindows()