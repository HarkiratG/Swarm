import numpy as np
import cv2
import math

# finds coordinates of the circle
def find_location(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    minR = 80;
    maxR = 125;
    # # # # # cv2.HoughCircles(image, method, dp, minDist)
    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT, 2, (2*.9)*minR,
        param1=150, param2=100, minRadius=minR, maxRadius=maxR) #150/100

    if circles is not None:
        circles = np.uint16(np.around(circles))
        # returns circles = [x_Centre y_centre radius]
        return circles

# find contours of color specified
def rangeContours(hsv, colorLower, colorUpper):
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # returns contours of the color speicified
    return cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# finds coordinates of the green orientation block
def find_orientation_block(frame):
    sensitivity = 50
    #bgr
    greenLower = (15, 85, 50)
    greenUpper = (50, 200, 130)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cont_frame, contours, hierarchy = rangeContours(frame,greenLower, greenUpper)
    centers = []
    
    for i, cont in enumerate(contours, start=0):
        M = cv2.moments(cont)
        centers.append( [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])] )
    # returns centres of green block + contours to plot it
    return [centers, contours]

# returns the location (of centre) + orientation of the robot
def find_robots(frame):
    circles                         = find_location(frame);
    (green_centre, green_contours)  = find_orientation_block(frame);
    robots = []
    if circles is not None:
        # print "Circles: "
        for i in circles[0,:]:
            cv2.circle(frame,(i[0],i[1]),i[2],(255,0,0),2); # draw the outer circle
            cv2.circle(frame,(i[0],i[1]),2,   (0,0,255),3); # draw the center of the circle
            # print i
            if len(green_centre) > 0:
                # print "Green"
                cv2.drawContours(frame, green_contours, -1, (0,255,0), 1) #draw green contours
                for j in green_centre:
                    # print j
                    cv2.circle(frame,(j[0],j[1]),2,(0,0,255),3); # draw the center of the green
                    x_delta = j[0] - i[0];
                    y_delta = j[1] - i[1];
                    distance = math.sqrt(math.pow(x_delta,2) + math.pow(y_delta,2));
                    angle = math.atan2(y_delta, x_delta) * 180/math.pi;
                    if (distance < i[2]*1.5):
                        robots.append([i[0], i[1], angle]);
                    # print distance, angle

    # returns stats on robots [x_pos; y_pos; angle]
    return robots


