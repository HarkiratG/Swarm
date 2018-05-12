import cv2
import math
import serial

import vision
from robotClass import *

target = [650,330]

roboot_distance = 230

cart1 = robot("/dev/cu.HC-05-DevB", target)
# cart2 = robot("/dev/cu.HC-05-DevB-1", target)
# cart3 = robot("/dev/cu.HC-05-DevB-2", target)

cam = cv2.VideoCapture(0)

if 0:
	print range(1,5) + range(11,15)

while 1:
	(got_frame, frame) = cam.read()

	a = vision.find_robots(frame)
	b = vision.get_target(frame)
	# vision.show_all(frame)
	print " "
	if a:
		print a
		cart1.current_position = a[0]
		cart1.move()
	else:
		print " cant see robot"
		cart1.stop()
	if b:
		print b
		target = b
		cart1.target_position = b
	#
	cv2.circle(frame,(target[0],target[1]),2,(0,255,0),3);
	cv2.imshow('frame', frame)
	cv2.waitKey(1)
#
cam.release()
cv2.destroyAllWindows()
