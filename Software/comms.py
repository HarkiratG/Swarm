import serial
import string

address1 = "/dev/cu.HC-05-DevB"
address2 = "/dev/cu.HC-05-DevB-1"

robo1 = serial.Serial(address1,9600)
robo2 = serial.Serial(address2,9600)

robo1.flushInput()
robo2.write('q')

while 1:
	robo1.write(raw_input("Prompt (1): "))
	robo1.flushInput()
	robo2.write(raw_input("Prompt (2): "))
	robo2.flushInput()
#
robo1.write('q')
robo1.close()

robo2.write('q')
robo2.close()