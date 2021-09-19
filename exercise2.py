'''
Lab 1: Introduction to Python for Embedded CPS
Student Name: Joe Vetere
MSU NetID: veterejo

This file 
'''

#%% Step 2
#Adding the equal signs/lines helps
#to organize the output between exercise steps
print("========= Step 2 ========= ")
sampleInteger = 5
exampleFloat = 5.0
simpleList = ["one", "two", 3, 4.0]
someString = "Lorem Ipsum"
emptyType = None

print(sampleInteger)
print(exampleFloat)
print(simpleList)
print(someString)
print(emptyType)

#adding two strings
resultingString = someString + "-additional"
print(resultingString)

# adding integers
resultingInteger = sampleInteger + 1
print(resultingInteger)

#adding integer and float
resultingNumber = sampleInteger + exampleFloat 
print(resultingNumber)

#adding integer and string
resultingObject = str(resultingInteger) + resultingString 
print(resultingObject)

print(5 * 5) #multiplying two integers - will return an integer
print(5.0 * 5.0) #multiplying two floats - will return a float
print(5**2) #exponent
print(5/2) #divsion between two integers
print(5.0/2) #division between an integer and float
print(5 % 2) #modulo operator
print( min(5, 10, 25) ) #finds the smallest number in a list
print( max(5, 10, 25) ) #finds the largest number in a list
print ( abs(-7.25) ) #absolute value of a number
print(round(3.123456, 2)) #rounds the float to 2 digits
print(sum([1,2,3])) #sums the list of numbers

import math #importing the math module
x = math.pi #get the value of pi
print(x)
print(math.sqrt(64)) #square root

#%% Step 3
print("========= Step 3 =========")
sampleList = [] #this is an empty list

listWithStrings = ["Item One", "Item Two", "Item Three"] #list with strings

listWithNumbers = [100, 200, 300, 400] #list with integers

print(sampleList)
print(listWithStrings)
print(listWithNumbers)

#adding lists
print(simpleList + sampleList)
print(listWithStrings + listWithNumbers)
print(sampleList + sampleList)

#removing items from the previously defined list
print(listWithStrings.pop(0))
print(listWithStrings.pop(1))
#adding another item
print(listWithStrings.append("Item Four"))
print(listWithStrings)

#%% Step 4
print("========= Step 4 ========= ")
my_name = "Joe"
another_name = "John"
number = 25

#one string
print("Hello %s" % my_name)

#two strings
print("Hello %s and %s" % (my_name, another_name) )

#print integer/ digit
print("Today is the %dth day of the month" % number)

myString = "hello world"

print(myString[0])
print(myString[0:2])
print(myString[1:9])
print(myString[0:0])
print(myString[0:-1]) #negative index starts at end of string and moves backward

#%% Step 5
print("========= Step 5 ========= ")
myVariable = 0

if myVariable < 1: #will first compare this condition
	myVariable += 1
elif myVariable > 1 and myVariable <5: #next if the above did not pass
	myVariable += 2
else: #will run this if none of the above passed
	myVariable = 2

print(myVariable)

count = 0
while (count < 5):
	print("The count is: %d" % count)
	count = count + 1
else:
	print('complete!')

#loop through a string
for letter in "hello world":
	print("Current Letter :", letter)


#loop through a range of numbers, while breaking once you reach 3
for i in range(1, 5):
	print(i)
	if i % 3 == 0: #modulo, returns the remainder of integer division
		break

#loop through a range of numbers and print only the even numbers
for i in range(1, 1001):
	if i % 2 == 0:
		print(i)

#%% Step 6
print("========= Step 6 ========= ")
# prints a list with the given name
def print_list(listParam , listName="Default List Name"):
	print(listName) #print the value passed for the list name
	for i in listParam:
		print(i)

result = print_list([100,200,300])

print(result)


'''
Slope of line can be calculated by:
m = rise/run = (y2 - y1)/(x2 - x1)

Line of best fit formula:
y = mx + b

Converted to solve for b
b = y1 - (m * x1)
'''

def findLine(x1, y1, x2, y2):
	#Slope of line
	m = (y2 - y1)/(x2 - x1)

	#Line of best fit
	b = y1 - (m * x1)

	#Format values to two decimals
	m = round(m,2)
	b = round(b,2)
	return m, b

m, b = findLine(4, 8, 10, 3)
print(m, b) #should return -0.83, 11.3

m, b = findLine(1.2, 1.4, 8.7, 7.2)
print(m, b) #should return 0.77, 0.47

#%% Step 7
print("========= Step 7 ========= ")

myDictionary = {} #defining an empty dictionary

#defining a dictionary with items 
#keys can be a string or integer
myDictionary = {
	"key1": "hello",
	"key2": "world"
}

print(myDictionary)
print(myDictionary["key1"]) #print out the value at "key1"

#you can change the value of a key in the dictionary with the below syntax
myDictionary["key1"] = "world"

#you can define a new key in the dictionary with the below syntax
myDictionary["key3"] = 123

print(myDictionary)

#%% Step 8
print("========= Step 8 ========= ")


"""
Grade Calculator Program
"""

#The main function containing the program code
#accepts a student’s records as list of dictionaries
#and will output the final course grade of the student
#in the form of a float (e.g., 92.67)
def calculateMyGrade(studentGradeslist):

	#first define the weight given to diff items
	GRADING = {
		"Exam": 0.6,
		"Homework": 0.1,
		"Project": 0.3
	}

	pointsScored = {"Exam": [], "Homework": [], "Project": []} #track the points the student got
	pointsPossible = {"Exam": [], "Homework": [], "Project": []} #track the points possible

	#loop through the student’s grades
	for i in studentGradeslist:
		if i["ItemType"] == "Exam":
			pointsScored["Exam"].append(i["Score"])
			pointsPossible["Exam"].append(i["MaximumPossibleScore"])
		elif i["ItemType"] == "Homework":
			pointsScored["Homework"].append(i["Score"])
			pointsPossible["Homework"].append(i["MaximumPossibleScore"])
		else:
			pointsScored["Project"].append(i["Score"])
			pointsPossible["Project"].append(i["MaximumPossibleScore"])

	
	#Sum the exam scores using sum()
	examWeightedScore = (GRADING["Exam"]*sum(pointsScored["Exam"])/float(sum(pointsPossible["Exam"])))
	
	#Remove dropped assignment from pointsScored and pointsPossible. Verifies value no longer exists and notifies student.
	pointsScored["Homework"].remove(0)
	print("Removed dropped homework assignment from total homework points scored. Scores recorded are: " + str(pointsScored["Homework"]))
	pointsPossible["Homework"].remove(0)
	print("Removed dropped homework assignment from total homework points possible. Possible points recorded are:" + str(pointsPossible["Homework"]))
	
	#Sum the homework scores using sum()
	homeworkWeightedScore = (GRADING["Homework"]*sum(pointsScored["Homework"])/float(sum(pointsPossible["Homework"])))
	
	#Sum the project scores using sum()
	projectWeightedScore = (GRADING["Project"]*sum(pointsScored["Project"])/float(sum(pointsPossible["Project"])))

	return examWeightedScore + homeworkWeightedScore + projectWeightedScore

#Find out a student’s grade by calling the function
student1Grades = [
	{"ItemType": "Exam",
	"Score": 92.55,
	"MaximumPossibleScore": 100},
	{"ItemType": "Exam",
	"Score": 72.15,
	"MaximumPossibleScore": 86},
	{"ItemType": "Homework",
	"Score": 32,
	"MaximumPossibleScore": 100},
	{"ItemType": "Homework",
	"Score": 0,
	"MaximumPossibleScore": 0},
	{"ItemType": "Homework",
	"Score": 93.122,
	"MaximumPossibleScore": 95},
	{"ItemType": "Project",
	"Score": 113,
	"MaximumPossibleScore": 157},
	{"ItemType": "Project",
	"Score": 176,
	"MaximumPossibleScore": 179}
]

#when printing the final grade, we round the results using
#the round() function, and then multiply by 100 to get a percentage
print("The final grade is: " + str(100*round(calculateMyGrade(student1Grades), 5) ))


