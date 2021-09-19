'''
Lab 1: Introduction to Python for Embedded CPS
Student Name: Joe Vetere
MSU NetID: veterejo

This file demonstrate how to use the simulation programs 
provided for the course in each lab, and briefly cover the 
core concepts of ROS to build a finite state machine (FSM). 
This exercise will also demonstrate how to use the library 
Matplotlib to plot data in Python.
'''

from ros_shim import rospy
from ros_shim import std_msgs
import time

NODENAME = "Lab 1 exercise 3 node"
rospy.init_node(NODENAME)
MAX_TEMP = 0.22
MIN_TEMP = 0.18

heaterPublisher = rospy.Publisher("/heater", std_msgs.String)

#print the data provided
#for ROS functions, you always need the data parameter
def my_function(data):
	if (data <= MIN_TEMP):
		heaterPublisher.publish("on") #turn on the heater is the temperature is below 18C ..
	else:
		heaterPublisher.publish("off")
	print(data)

thermostatSub = rospy.Subscriber("/thermostat", std_msgs.Int64, my_function)

time.sleep(10)

thermostatSub.unregister() #this unregisters the ROS node from reading data. If not called , will continue to run the name plt

#%% Code to create a plot
import math
import matplotlib.pyplot as plt #this will import the matplotlib library under

plt.xlabel("Time") #sets the x-axis label
plt.ylabel("Temperature") #sets the y-axis label
plt.title("Temperature vs. Time") #sets the title

#this draw a horizontal line on the graph #to show a threshold value plt.axhline(y=0.1, color=’r’, linestyle=’-’) plt.axhline(y=0.5, color=’r’, linestyle=’-’)
#this is temp data to be plotted
data_to_be_plotted = [
0.5,0.45,0.2,0.3,0.6
]

#plt.plot(x,y)
plt.plot(list(range(0,len(data_to_be_plotted))),data_to_be_plotted)
plt.show() #calling this will show the plot in the output