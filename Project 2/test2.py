import time
from robomaster import robot
from robomaster import vision
from robomaster import led


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_version = ep_robot.get_version()
    print("Robot Version: {0}".format(ep_version))
    SN = ep_robot.get_sn()
    print("Robot SN:", SN)

    ep_led = ep_robot.led
    ep_vision = ep_robot.vision

    #Configure robot movement mode to GIMBAL_LEAD.
    ep_robot.set_robot_mode(mode=robot.GIMBAL_LEAD)
    #Configure robot vision mode to follow blue line.
    ep_vision.sub_detect_info("line", color="blue", callback=None)

    variable_x = 0 #X Position
    variable_v = 0 #Velocity
    variable_V_average = 0 #Average speed in the line following procedure
    variable_K = 0 #Proportional coefficient that adjusts the speed according to the actual tangential angle during the line following procedure. KEY TO SPEED ADJUSTMENT
    PID_Follow_Line = [] #Proportional Integral Drive Controller (or 3-term controller) - control loop mechanism employing feedback for (in this case) targetting and positioning (maybe localization?) for line follow.
    LineList = [] #Track information

    

    #Implement 8 brightness changes of the LED light, each of which lasts for 1 second
    bright = 1
    for i in range(0, 8):
    	ep_led.set_led(comp=led.COMP_ALL, r=bright << i, g=bright << i, b=bright << i, effect=led.EFFECT_ON)
    	time.sleep(.15)
    	print("brightness: {0}".format(bright << i))


    ep_chassis = ep_robot.chassis

    x_val = 0.5
    y_val = 0.3
    z_val = 30

    # Forward
    ep_chassis.drive_speed(x=x_val, y=0, z=0, timeout=5)
    time.sleep(3)

    # Backward
    ep_chassis.drive_speed(x=-x_val, y=0, z=0, timeout=5)
    time.sleep(3)

    # Slide Left
    ep_chassis.drive_speed(x=0, y=-y_val, z=0, timeout=5)
    time.sleep(3)

    # Slide Right
    ep_chassis.drive_speed(x=0, y=y_val, z=0, timeout=5)
    time.sleep(3)

    # Rotate Counter-Clockwise
    ep_chassis.drive_speed(x=0, y=0, z=-z_val, timeout=5)
    time.sleep(3)

    # Rotate Clockwise
    ep_chassis.drive_speed(x=0, y=0, z=z_val, timeout=5)
    time.sleep(3)

    # 停止麦轮运动
    ep_chassis.drive_speed(x=0, y=0, z=0, timeout=5)

    ep_robot.close()