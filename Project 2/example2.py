import time
from robomaster import robot
from robomaster import led


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_version = ep_robot.get_version()
    print("Robot Version: {0}".format(ep_version))
    SN = ep_robot.get_sn()
    print("Robot SN:", SN)

    ep_chassis = ep_robot.chassis
    ep_led = ep_robot.led

    x_val = 0.5
    y_val = 0.6
    z_val = 90

    ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
    time.sleep(1)

    chassis_action = ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7)
    ep_led.set_led(comp=led.COMP_ALL, r=0, g=255, b=0, effect=led.EFFECT_ON)
    chassis_action.wait_for_completed()

    ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7)
    ep_led.set_led(comp=led.COMP_ALL, r=0, g=0, b=255, effect=led.EFFECT_ON)
    time.sleep(10)

    ep_robot.close()