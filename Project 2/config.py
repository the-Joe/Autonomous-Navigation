import robomaster
from robomaster import robot


if __name__ == '__main__':
    ep_robot = robot.Robot()

    ep_robot.initialize(conn_type='sta', proto_type='udp')

    version = ep_robot.get_version()
    print("Robot Version: {0}".format(version))
    ep_robot.close()
