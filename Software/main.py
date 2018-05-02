import cv2
import math
import serial

import vision
from robotClass import *

target = [650,330]

cart1 = robot("/dev/cu.HC-05-DevB", target)

cam = cv2.VideoCapture(0)

if 0:
	print range(1,5) + range(11,15)

while 1:
	(got_frame, frame) = cam.read()

	a = vision.find_robots(frame)
	print " "
	if a:
		cart1.current_position = a[0]
		cart1.move()
	else:
		cart1.stop()
		print " cant see robot"

	#
	cv2.circle(frame,(target[0],target[1]),2,(0,0,255),3);
	cv2.imshow('frame', frame)
	cv2.waitKey(0)
#
cam.release()
cv2.destroyAllWindows()
