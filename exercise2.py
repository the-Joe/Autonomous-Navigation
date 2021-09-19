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

