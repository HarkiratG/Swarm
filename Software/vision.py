import numpy as np
import cv2
import math

# finds coordinates of the circle
def find_location(frame):
    cont_frame, contours, hierarchy = rangeContours(frame, (210, 210, 210), (255, 255, 255))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray', gray)
    circles = []
    minR = 40;
    maxR = 80;

    for i, cnt in enumerate(contours, start=0):
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        centre = (int(x), int(y))
        radius = int(radius)
        a = cv2.contourArea(cnt)
        if math.pi*minR*minR < a < math.pi*maxR*maxR:
            circles.append([centre[0], centre[1], radius])
    # returns stats (centre, area) of green block + contours to plot it
    return circles


    # # # # # cv2.HoughCircles(image, method, dp, minDist)
    # circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT, 2, (2*.9)*minR,
    #     param1=150, param2=100, minRadius=minR, maxRadius=maxR) #150/100

    # if circles is not None:
    #     circles = np.uint16(np.around(circles))
    # # returns circles = [x_Centre y_centre radius]
    # print circles

# find contours of color specified
def rangeContours(hsv, colorLower, colorUpper):
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # returns contours of the color speicified
    return cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# find targeted ball
def find_ball(frame):
    sensitivity = 50
    #bgr
    redLower = (0, 0, 150)
    redUpper = (100, 100, 255)

    cont_frame, contours, hierarchy = rangeContours(frame, redLower, redUpper)
    # centers = []
    
    for i, cnt in enumerate(contours, start=0):
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        centre = (int(x), int(y))
        radius = int(radius)
        a = cv2.contourArea(cnt)

        minR = 20;
        maxR = 80;

        if math.pi*minR*minR < a < math.pi*maxR*maxR:
            return [centre[0], centre[1], radius]

# returns the location (of centre) + orientation of the robot
def get_target(frame):
    ball_centre  = find_ball(frame);
    if ball_centre:
        # for j, i in enumerate(ball_centre):
        # cv2.circle(frame, (ball_centre[0],ball_centre[1]),ball_centre[2],(0,0,255),2); # draw the outer circle
        # cv2.circle(frame, (ball_centre[0],ball_centre[1]),2,   (0,255,0),3); # draw the center of the circle
            # cv2.drawContours(frame, ball_contour, -1, (0,0,255), 1) #draw red contours

        # returns ball centres
        return [ball_centre[0], ball_centre[1]]

# finds coordinates of the green orientation block
def find_orientation_block(frame):
    sensitivity = 50
    #bgr
    greenLower = (90, 170, 50)
    greenUpper = (190, 255, 160)

    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cont_frame, contours, hierarchy = rangeContours(frame, greenLower, greenUpper)
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
    for j, i in enumerate(circles):
        if len(green_centre) > 0:
            for j in green_centre:
                x_delta = i[0] - j[0];
                y_delta = i[1] - j[1];
                distance = math.hypot(x_delta, y_delta);
                angle = math.atan2(y_delta, x_delta) * 180/math.pi;
                # only mates the green blocks to close by circle
                if (distance < i[2]*1.5): 
                    robots.append([i[0], i[1], angle]);
                    cv2.circle(frame, (i[0],i[1]),i[2],(255,0,0),2); # draw the outer circle
                    cv2.circle(frame, (i[0],i[1]),2,   (0,0,255),3); # draw the center of the circle
                    cv2.circle(frame,(j[0],j[1]),2,(0,0,255),3); # draw the center of the green
                    cv2.drawContours(frame, green_contours, -1, (0,255,0), 1) #draw green contours

    # returns stats on robots [x_pos; y_pos; angle]
    return robots


