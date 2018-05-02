import serial
import string
import math

class robot:

	address = "/dev/cu.HC-05-DevB"
	speed = 0;
	speedlimit = 1;
	current_position = [0,0,0]
	target_position = [0, 0]
	distance = 0;
	angle_diff = 0;
	quadrant = 0;

	def __init__ (self, address, target):
		self.address = address
		self.target_position = target
	#
	port = serial.Serial(address, 9600)

	# method to move the robot
	def move(self):
		self.calc_dist_angle()

		print "angle ", self.angle_diff, "distance", self.distance

		if 30 <= abs(self.angle_diff) <= 90: 
			self.orient()

		elif self.distance > 50:
			if 160 <= abs(self.angle_diff) <= 200:
				self.forward()
			elif abs(self.angle_diff) <= 20 or 340 <= abs(self.angle_diff) <= 360:
				self.backward()
		#
		else:
			self.stop();

	# method to move the robot forward
	def forward(self):
		ratio = int(math.ceil((self.distance*8)/1000))
		if self.speed < 2:
			# for i in range(0,ratio):
			print "forward ", ratio, self.speed
			# self.port.write("w")
			self.speed = self.speed+1;

	# method to move the robot backward
	def backward(self):
		ratio = int(math.ceil((self.distance*8)/1000))
		if self.speed > -2:
			print "backward", ratio, self.speed
			# for i in range(0,ratio):
				# self.port.write("s")
			self.speed = self.speed-1;

	# method to stop the robot
	def stop(self):
		print "stopped"
		self.port.write("q")
		self.speed = 0

	# method to find the required orientation
	def orient(self):
		if (self.angle_diff > 20) and (self.speed < 1):
			print "left"
			# self.port.write("a")
			self.speed = self.speed + 1
		elif (self.angle_diff < -20) and (self.speed < 1):
			print "right"
			# self.port.write("d")
			self.speed = self.speed + 1

	# method to calculate the distance and orientation difference
	def calc_dist_angle(self):
		x_delta = self.target_position[0] - self.current_position[0]
		y_delta = self.target_position[1] - self.current_position[1]
		self.distance = math.hypot(x_delta, y_delta)

		required_orientation = math.atan2(y_delta, x_delta) * 180/math.pi 
		current_orientation = self.current_position[2]
		# 
		# if required_orientation < 0:
		# 	required_orientation = 360 + required_orientation
		
		# if current_orientation < 0:
		# 	current_orientation = 360 + current_orientation
		#
		self.angle_diff = (required_orientation - current_orientation)

		print required_orientation, current_orientation, self.angle_diff
