import sys
import robomaster
from robomaster import action
from robomaster import algo
from robomaster import armor
from robomaster import battery
from robomaster import blaster
from robomaster import camera
from robomaster import chassis
from robomaster import client
from robomaster import config
from robomaster import conn
from robomaster import dds
from robomaster import event
from robomaster import exceptions
from robomaster import flight
from robomaster import gimbal
from robomaster import gripper
from robomaster import led
from robomaster import media
from robomaster import module
from robomaster import protocol
from robomaster import robot
from robomaster import robotic_arm
from robomaster import sensor
from robomaster import servo
from robomaster import uart
from robomaster import util
from robomaster import version
from robomaster import vision

orig_stdout = sys.stdout
f = open('robomaster_help.txt', 'w')
sys.stdout = f

print(help(action))
print(help(algo))
print(help(armor))
print(help(battery))
print(help(blaster))
print(help(camera))
print(help(chassis))
print(help(client))
print(help(config))
print(help(conn))
print(help(dds))
print(help(event))
print(help(exceptions))
print(help(flight))
print(help(gimbal))
print(help(gripper))
print(help(led))
print(help(media))
print(help(module))
print(help(protocol))
print(help(robot))
print(help(robotic_arm))
print(help(sensor))
print(help(servo))
print(help(uart))
print(help(util))
print(help(version))
print(help(vision))

sys.stdout = orig_stdout
f.close()