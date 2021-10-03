'''
Lab 2: Introduction to Python for Embedded CPS
Student Name: Joe Vetere
MSU NetID: veterejo

This file implements and simulates a garage counter based on the finite state machine
'''

from ros_shim import rospy

global c #Global variable that maintains the number of cars in the garage


nodeName = "Lab 2: Exercise 2"
rospy.init_node(nodeName)