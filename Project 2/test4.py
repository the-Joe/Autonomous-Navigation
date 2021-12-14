

import cv2
import time
import robomaster
from robomaster import camera
from robomaster import chassis
from robomaster import led
from robomaster import robot
from robomaster import vision

global state
line = []

class PointInfo:

    def __init__(self, x, y, theta, c):
        self._x = x
        self._y = y
        self._theta = theta
        self._c = c

    @property
    def pt(self):
        return int(self._x * 1280), int(self._y * 720)

    @property
    def color(self):
        return 255, 255, 255



def on_detect_line(line_info):
    global state
    global Xpos
    global Ypos
    global Zpos
    global Curv
    Xpos = 0
    Ypos = 0
    Zpos = 0
    Curv = 0
    number = len(line_info)
    line.clear()
    line_type = line_info[0]
    for i in range(1, number):
        x, y, theta, c = line_info[i]
        line.append(PointInfo(x, y, theta, c))
        Xpos = x
        Ypos = y
        Zpos = theta
        Curv = c


if __name__ == '__main__':
    global state
    global Xpos
    global Ypos
    global Zpos
    global Curv

    state = "Initializing"

    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_robot.set_robot_mode(mode=robot.GIMBAL_LEAD)


    ep_version = ep_robot.get_version()
    print("Robot Version: {0}".format(ep_version))
    SN = ep_robot.get_sn()
    print("Robot SN:", SN)

    print("*** Current System State: " + state + " ***")


    ep_led = ep_robot.led
    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis
    

    #Implement 8 brightness changes of the LED light, each of which lasts for 1 second
    bright = 1
    for i in range(0, 8):
        ep_led.set_led(comp=led.COMP_ALL, b=bright << i, effect=led.EFFECT_ON)
        time.sleep(.15)

    ep_camera.start_video_stream(display=False)
    state = "Analyzing Route"

    if state == "Analyzing Route":
        print("*** Current System State: " + state + " ***")
        result = ep_vision.sub_detect_info(name="line", color="blue", callback=on_detect_line)
        #Implement 8 brightness changes of the LED light, each of which lasts for 1 second
        bright = 1
        for l in range(0, 8):
            ep_led.set_led(comp=led.COMP_ALL, g=bright << l, b=bright << l, effect=led.EFFECT_ON)
        for i in range(0, 200):
            img = ep_camera.read_cv2_image(strategy="newest", timeout=0.5)

            for j in range(0, len(line)):
                cv2.circle(img, line[j].pt, 3, line[j].color, -1)
                
            cv2.imshow("Line", img)
            cv2.waitKey(1)
            state = "Autonomous"

            if state == "Autonomous":
                if len(line) > 0:
                    print("*** Current System State: " + state + " ***")
                    for r in range(0, 8):
                        ep_led.set_led(comp=led.COMP_ALL, g=bright << r, effect=led.EFFECT_ON)
                    ep_chassis.move(Ypos, 0, -Zpos, xy_speed = 1.5).wait_for_completed()
                else:
                    state = "Course Correction"
                    print("*** Current System State: " + state + " ***")
                    for w in range(0, 8):
                        ep_led.set_led(comp=led.COMP_ALL, r=bright << w, effect=led.EFFECT_ON)
                    ep_chassis.drive_speed(x=0, y=0, z=-30, timeout=5)
                    time.sleep(1)
                
    
    cv2.destroyAllWindows()
    result = ep_vision.unsub_detect_info(name="line")
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()