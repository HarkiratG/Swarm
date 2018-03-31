import cv2
import math

import vision
import comms

cam = cv2.VideoCapture(0)

while 1:
	(got_frame, frame) = cam.read()

	a = vision.find_robots(frame)

	print a

	cv2.imshow('frame', frame)

	cv2.waitKey(0)
#
cam.release()
cv2.destroyAllWindows()
