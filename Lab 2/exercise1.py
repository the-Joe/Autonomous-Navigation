'''
Lab 2: Introduction to Python for Embedded CPS
Student Name: Joe Vetere
MSU NetID: veterejo

This file will use ROS to receive sensor data from the robot 
and Python to parse and control the stationary robot in  order for it 
to follow the Sphero Mini.
'''

from ros_shim import rospy
from ros_shim import sensor_msgs , geometry_msgs , nav_msgs , std_msgs
import time #not ROS, but will be used later

#global variables
global leaderPos #hold position of the leader
global followerPos #hold position of the follower

#time variables
starttime = time.time()
endtime = 0
elapsedtime = endtime - starttime

nodeName = "Lab 2 Node" #can be any string
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

#print the data provided
#for ROS functions, you always need the data parameter

#leader function odometry
def leader_odom(data): 
	global leaderPos #need to set this to state we are using the global variable
	leaderPos = data #update the position with the retrieved data

# will return the x and y velocities to get to the (x2, y2) point from (x1, y1)
def determine_velocity_to_travel(x1, x2, y1, y2): 
	xVel = 0
	yVel = 0

	#enter your code to calculate the velocity of the robot here 
	xVel = (x2 - x1)/elapsedtime
	yVel = (y2 - y1)/elapsedtime

	return (xVel, yVel) #returns both velocities


#updated follower function
def follower_odom(data): 
	global followerPos
	global leaderPos 
	followerPos = data
	leaderPos = data

	#initialize the velocities
	xVel = 10 
	yVel = 10

	followerX = followerPos["pose"]["position"]["x"] #gets X-coord of follower 
	leaderX = leaderPos["pose"]["position"]["x"] #gets X-coord of leader 
	followerY = followerPos["pose"]["position"]["y"] #gets Y-coord of follower 
	leaderY = leaderPos["pose"]["position"]["y"] #gets Y-coord of leader


	#call your function
	xVel, yVel = determine_velocity_to_travel( 
		followerX ,
		leaderX , 
		followerY , 
		leaderY
		)

	#publish the calculated velocity to the robot
	changeVelocity.publish({ 
		"angular": {"z": 0},
		"linear": {
			"x": xVel ,
			"y": yVel

	}})

#attach these function to the ROS subscribers
#the syntax and meaning of these lines are further covered in the next lab 
rospy.Subscriber("/follower/odom", nav_msgs.Odometry , follower_odom) 
rospy.Subscriber("/leader/odom", nav_msgs.Odometry , leader_odom)


endtime = time.time()
time.sleep(5)


