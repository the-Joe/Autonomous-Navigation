import time
from robomaster import robot
from robomaster import camera
import cv2


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")


    ep_version = ep_robot.get_version()
    print("Robot Version: {0}".format(ep_version))
    SN = ep_robot.get_sn()
    print("Robot SN:", SN)

    ep_camera = ep_robot.camera

    # 显示200帧图传
    ep_camera.start_video_stream(display=False)
    for i in range(0, 10):
        img = ep_camera.read_cv2_image()
        cv2.imshow("Robot", img)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()

    ep_robot.close()