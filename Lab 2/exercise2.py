'''
Lab 2: Introduction to Python for Embedded CPS
Student Name: Joe Vetere
MSU NetID: veterejo

This file implements and simulates a garage counter based on the finite state machine
'''

from ros_shim import rospy
from ros_shim import sensor_msgs , geometry_msgs , nav_msgs , std_msgs
import time #not ROS, but will be used later

global c #Global variable that maintains the number of cars in the garage
global upState #Global variable for capturing the up state of the system
global downState #Global variable for capturing the down state of the system


nodeName = "Lab 2: Exercise 2"
rospy.init_node(nodeName)

c = 100
M = 100


#publisher variable
updateCount = rospy.Publisher("/count_update", std_msgs.Int64)

def upStateGarage(data): 
	global c
	global upState
	upState = data
	if upState == 1 and c < M:
		c = c + 1
		updateCount.publish(c)
		print("The current vehicle count in the garage is: " + str(c) + ". One car has entered to park.")
	elif upState == 1 and c >= M:
		print("You dummy, there's no more room here!")
	else:
		print("No additional cars parked.")

def downStateGarage(data): 
	global c
	global downState
	downState = data
	if downState == 1 and c > 0:
		c = c - 1
		updateCount.publish(c)
		print("The current vehicle count in the garage is: " + str(c) + ". One car left.")
	else:
		print("No cars left.")


#ROS subscriber functions
rospy.Subscriber("/up", std_msgs.Bool , upStateGarage) #Indicates presence of car in the up position (for addition to count)
rospy.Subscriber("/down", std_msgs.Bool , downStateGarage) #Indicates presence of car in the down position (for subrtaction to count)
#rospy.Subscriber("/count", std_msgs.Int64 , garageCounter) #Current count

time.sleep(100)