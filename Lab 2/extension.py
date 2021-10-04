'''
Lab 2: Introduction to Python for Embedded CPS
Student Name: Joe Vetere
MSU NetID: veterejo

This file implements and simulates a garage counter based on the finite state machine
'''

from ros_shim import rospy
from ros_shim import sensor_msgs , geometry_msgs , nav_msgs , std_msgs
import time #not ROS, but will be used later


global upState #Global variable for capturing the up state of the system
global downState #Global variable for capturing the down state of the system
global firstFloor #1st floor dictionary for garage.
global secondFloor #2nd floor dictionary for garage.
global thirdFloor #3rd floor dictionary for garage.
global fourthFloor #4th floor dictionary for garage.
global vacantSpots
global occupiedSpots

firstFloor = {"Space 1":"Occupied","Space 2":"Occupied","Space 3":"Occupied","Space 4":"Vacant","Space 5":"Vacant"}
secondFloor = {"Space 1":"Occupied","Space 2":"Occupied","Space 3":"Occupied","Space 4":"Occupied","Space 5":"Vacant"}
thirdFloor = {"Space 1":"Vacant","Space 2":"Occupied","Space 3":"Vacant","Space 4":"Occupied","Space 5":"Vacant"}
fourthFloor = {"Space 1":"Occupied","Space 2":"Vacant","Space 3":"Vacant","Space 4":"Occupied","Space 5":"Occupied"}
vacantSpots = []
occupiedSpots = []


nodeName = "Lab 2: Extension"
rospy.init_node(nodeName)

def upStateGarage(data):
	global upState
	global firstFloor
	global secondFloor
	global thirdFloor
	global fourthFloor
	global vacantSpots
	upState = data

	if upState == 1:
		print("Someone has entered the garage.")
		if "Vacant" in firstFloor.values():
			for key, value in firstFloor.items():
				if "Vacant" == value:
					vacantSpots.append(key)
			print("The following spaces are available on the first floor: " + str(vacantSpots))
			firstFloor[vacantSpots[0]] = "Occupied" # Sets first available space in the list as occupied in the dictionary for this floor
			print(vacantSpots[0] + " on the First Floor is now occupied.")
			vacantSpots = [] # Clear the list for future use.
		elif "Vacant" in secondFloor.values():
			print ("There are currently no open spaces on the first floor.")
			for key, value in secondFloor.items():
				if "Vacant" == value:
					vacantSpots.append(key)
			print("The following spaces are available on the second floor: " + str(vacantSpots))
			secondFloor[vacantSpots[0]] = "Occupied" # Sets first available space in the list as occupied in the dictionary for this floor
			print(vacantSpots[0] + " on the Second Floor is now occupied.")
			vacantSpots = [] # Clear the list for future use.
		elif "Vacant" in thirdFloor.values():
			print ("There are currently no open spaces on the first or second floor.")
			for key, value in thirdFloor.items():
				if "Vacant" == value:
					vacantSpots.append(key)
			print("The following spaces are available on the third floor: " + str(vacantSpots))
			thirdFloor[vacantSpots[0]] = "Occupied" # Sets first available space in the list as occupied in the dictionary for this floor
			print(vacantSpots[0] + " on the Third Floor is now occupied.")
			vacantSpots = [] # Clear the list for future use.
		elif "Vacant" in fourthFloor.values():
			print ("There are currently no open spaces on the first, second or third floor.")
			for key, value in fourthFloor.items():
				if "Vacant" == value:
					vacantSpots.append(key)
			print("The following spaces are available on the fourth floor: " + str(vacantSpots))
			fourthFloor[vacantSpots[0]] = "Occupied" # Sets first available space in the list as occupied in the dictionary for this floor
			print(vacantSpots[0] + " on the Fourth Floor is now occupied.")
			vacantSpots = [] # Clear the list for future use.
		else:
			print("Sorry, we have no available spots at this time. Customer must exit the garage.")

def downStateGarage(data):
	global downState
	global firstFloor
	global secondFloor
	global thirdFloor
	global fourthFloor
	global occupiedSpots
	downState = data

	if downState == 1:
		print("Someone has left the garage.")
		if "Occupied" in firstFloor.values():
			for key, value in firstFloor.items():
				if "Occupied" == value:
					occupiedSpots.append(key)
			firstFloor[occupiedSpots[0]] = "Vacant" # Sets first occupied space in the list as vacant in the dictionary for this floor
			print("Their space was on the first floor. The following spaces on the First Floor are now vacant:")
			for key, value in firstFloor.items():
				if "Vacant" == value:
					print(key)
			occupiedSpots = [] # Clear the list for future use.
		elif "Occupied" in secondFloor.values():
			for key, value in secondFloor.items():
				if "Occupied" == value:
					occupiedSpots.append(key)
			secondFloor[occupiedSpots[0]] = "Vacant" # Sets first occupied space in the list as vacant in the dictionary for this floor
			print("Their space was on the Second Floor. The following spaces on the Second Floor are now vacant:")
			for key, value in secondFloor.items():
				if "Vacant" == value:
					print(key)
			occupiedSpots = [] # Clear the list for future use.
		elif "Occupied" in thirdFloor.values():
			for key, value in thirdFloor.items():
				if "Occupied" == value:
					occupiedSpots.append(key)
			thirdFloor[occupiedSpots[0]] = "Vacant" # Sets first occupied space in the list as vacant in the dictionary for this floor
			print("Their space was on the Third Floor. The following spaces on the Third Floor are now vacant:")
			for key, value in thirdFloor.items():
				if "Vacant" == value:
					print(key)
			occupiedSpots = [] # Clear the list for future use.
		elif "Occupied" in fourthFloor.values():
			for key, value in fourthFloor.items():
				if "Occupied" == value:
					occupiedSpots.append(key)
			fourthFloor[occupiedSpots[0]] = "Vacant" # Sets first occupied space in the list as vacant in the dictionary for this floor
			print("Their space was on the Fourth Floor. The following spaces on the Fourth Floor are now vacant:")
			for key, value in fourthFloor.items():
				if "Vacant" == value:
					print(key)
			occupiedSpots = [] # Clear the list for future use.
		else:
			print("The garage is totally vacant. No one could have left. Check the sensors for fault.")
		

#ROS subscriber functions
rospy.Subscriber("/up", std_msgs.Bool , upStateGarage) #Indicates presence of car in the up position (for addition to count)
rospy.Subscriber("/down", std_msgs.Bool , downStateGarage) #Indicates presence of car in the down position (for subrtaction to count)

time.sleep(30)
'''
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

time.sleep(10)
'''