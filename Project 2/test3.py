import cv2
import time
import robomaster
from robomaster import robot
from robomaster import vision
from robomaster import led


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


line = []


def on_detect_line(line_info):
    global Xpos
    global Ypos
    global Zpos
    Xpos = 0
    Ypos = 0
    Zpos = 0
    number = len(line_info)
    line.clear()
    line_type = line_info[0]
    for i in range(1, number):
        x, y, theta, c = line_info[i]
        line.append(PointInfo(x, y, theta, c))
        Xpos = x
        Ypos = y
        Zpos = theta



if __name__ == '__main__':
    global Xpos
    global Ypos
    global Zpos
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_version = ep_robot.get_version()
    print("Robot Version: {0}".format(ep_version))
    SN = ep_robot.get_sn()
    print("Robot SN:", SN)

    ep_led = ep_robot.led
    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis
    

    #Implement 8 brightness changes of the LED light, each of which lasts for 1 second
    bright = 1
    for i in range(0, 8):
        ep_led.set_led(comp=led.COMP_ALL, r=bright << i, g=bright << i, b=bright << i, effect=led.EFFECT_ON)
        time.sleep(.15)
        print("brightness: {0}".format(bright << i))

    ep_camera.start_video_stream(display=False)
    result = ep_vision.sub_detect_info(name="line", color="blue", callback=on_detect_line)

    for i in range(0, 1500):
        img = ep_camera.read_cv2_image(strategy="newest", timeout=0.5)
        for j in range(0, len(line)):
            cv2.circle(img, line[j].pt, 3, line[j].color, -1)
        cv2.imshow("Line", img)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    result = ep_vision.unsub_detect_info(name="line")
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()


    
