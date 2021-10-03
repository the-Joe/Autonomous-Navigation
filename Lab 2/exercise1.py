'''
Lab 2: Introduction to Python for Embedded CPS
Student Name: Joe Vetere
MSU NetID: veterejo

This file will use ROS to receive sensor data from the robot 
and Python to parse and control the stationary robot in order for it 
to follow the leader robot.
'''

from ros_shim import rospy
from ros_shim import sensor_msgs , geometry_msgs , nav_msgs , std_msgs
import time #not ROS, but will be used later

#global variables
global leaderPos #hold position of the leader
global followerPos #hold position of the follower
global starttime
global endtime
global elapsedtime
global leaderX
global followerX
global leaderY
global followerY

#time variables
starttime = time.time()
endtime = 0

nodeName = "Lab 2: Exercise 1" #can be any string
rospy.init_node(nodeName)

# a function to view the current published topics
def view_topics():
	topics = rospy.get_published_topics() #function provided in ROS library 
	for t in topics: #loop through the topics and print them
		print("Topic: {} Message Type: {}".format(t[0], t[1]))


#then call the function
print(view_topics())

#publisher variable
changeVelocity = rospy.Publisher("/cmd_vel", geometry_msgs.Twist)

delta_distance = [] #List to hold delta distance data collected between the robots
time_readings = [] #List to hold data collection time in seconds

#leader function odometry
def leader_odom(data): 
	global leaderPos #need to set this to state we are using the global variable
	leaderPos = data #update the position with the retrieved data

# will return the x and y velocities to get to the (x2, y2) point from (x1, y1)
def determine_velocity_to_travel(x1, x2, y1, y2): 
	global followerPos
	global leaderPos
	global starttime
	global endtime
	global elapsedtime
	global leaderX
	global followerX
	global leaderY
	global followerY

	#enter your code to calculate the velocity of the robot here 
	endtime = time.time()
	

	xVel = (x2 - x1)/elapsedtime
	yVel = (y2 - y1)/elapsedtime

	if xVel == 0 and followerX < 500:
		xVel = abs(leaderX - followerX)/elapsedtime
	elif followerX == 500:
		xVel = -abs(leaderX - followerX)/elapsedtime
	else:
		print("I'm already on my way on the X-Axis! My linear speed is " + str(abs(xVel)) + " m/s")
		delta_distance.append(abs(leaderX - followerX))
		time_readings.append(time.time() - starttime)

	if yVel == 0 and followerY < 750:
		yVel = abs(leaderY - followerY)/elapsedtime
	elif followerX == 750:
		xVel = -abs(leaderY - followerY)/elapsedtime
	else:
		print("I'm already on my way on the Y-Axis! My linear speed is " + str(abs(xVel)) + " m/s")

	return (xVel, yVel) #returns both velocities

#updated follower function
def follower_odom(data): 
	global followerPos
	global leaderPos
	global starttime
	global endtime
	global elapsedtime
	global leaderX
	global followerX
	global leaderY
	global followerY
	followerPos = data

	#initialize the velocities
	xVel = 1 
	yVel = 1

	followerX = followerPos["pose"]["position"]["x"] #gets X-coord of follower 
	leaderX = leaderPos["pose"]["position"]["x"] #gets X-coord of leader 
	followerY = followerPos["pose"]["position"]["y"] #gets Y-coord of follower 
	leaderY = leaderPos["pose"]["position"]["y"] #gets Y-coord of leader

	elapsedtime = endtime - starttime

	#call your function
	xVel, yVel = determine_velocity_to_travel(followerX, leaderX, followerY, leaderY)
	

	#publish the calculated velocity to the robot
	changeVelocity.publish({ 
		"angular": {"z": 0},
		"linear": {
			"x": xVel ,
			"y": yVel

	}})

	return (xVel, yVel) #returns both velocities

#attach these function to the ROS subscribers
#the syntax and meaning of these lines are further covered in the next lab 
rospy.Subscriber("/follower/odom", nav_msgs.Odometry , follower_odom) 
rospy.Subscriber("/leader/odom", nav_msgs.Odometry , leader_odom)



time.sleep(10)

import math
import matplotlib.pyplot as plt

plt.xlabel("Time") #sets the x-axis label
plt.ylabel("Distance") #sets the y-axis label
plt.title("Distance Over Time Between Follower & Leader") #sets the title

y = [delta_distance]
x = [time_readings]

#This plot tracks distance over time between the follower and the leader over the X-Axis of the simulation field
plt.plot(time_readings, delta_distance) #plt.plot(x,y) 
#plt.show() #calling this will show the plot in the output

plt.savefig("plot.png")