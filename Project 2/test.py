import time
from robomaster import robot
from robomaster import camera
import cv2








if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_version = ep_robot.get_version()
    print("Robot Version: {0}".format(ep_version))
    SN = ep_robot.get_sn()
    print("Robot SN:", SN)

    global variable_V_average
    global variable_shotTime
    global variable_device_qn
    global variable_markerPosX
    global variable_theta
    global variable_markerPosY
    global variable_max
    global variable_Maker
    global variable_b
    global variable_mode
    global variable_c
    global variable_pidout
    global variable_pitchVal
    global variable_n
    global variable_markerSizeW
    global variable_MarkerSizeH
    global variable_i
    global variable_x
    global variable_X
    global variable_Y
    global variable_K
    global variable_v
    global list_LineList
    global list_MarkerList
    global list_k
    global list_m
    global pid_pid
    global pid_cpst
    global pid_speed
    global pid_pitch
    global pid_Follow_Line
    variable_V_average = 0
    variable_shotTime = 0
    variable_device_qn = 0
    variable_markerPosX = 0
    variable_theta = 0
    variable_markerPosY = 0
    variable_max = 0
    variable_Maker = 0
    variable_b = 0
    variable_mode = 0
    variable_c = 0
    variable_pidout = 0
    variable_pitchVal = 0
    variable_n = 0
    variable_markerSizeW = 0
    variable_MarkerSizeH = 0
    variable_i = 0
    variable_x = 0
    variable_X = 0
    variable_Y = 0
    variable_K = 0
    variable_v = 0
    list_LineList = []
    list_MarkerList = []
    list_k = []
    list_m = []
    pid_pid = []
    pid_cpst = []
    pid_speed = []
    pid_pitch = []
    pid_Follow_Line = []
    
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    vision_ctrl.enable_detection(rm_define.vision_detection_line)
    vision_ctrl.line_follow_color_set(rm_define.line_follow_color_blue)
    variable_V_average = 1
    variable_K = 0.65
    pid_Follow_Line.set_ctrl_params(330,0,28)
    while True:
        list_LineList=RmList(vision_ctrl.get_line_detection_info())
        if len(list_LineList) == 42:
            if list_LineList[2] >= 1:
                robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
                variable_x = list_LineList[19]
                pid_Follow_Line.set_error(variable_x - 5)
                chassis_ctrl.rotate_with_speed(rm_define.clockwise,30)
                variable_v = variable_V_average - variable_K * abs(list_LineList[37] / 180)
                chassis_ctrl.set_trans_speed(variable_v)
                chassis_ctrl.move(0)
        else:
            chassis_ctrl.rotate_with_speed(rm_define.clockwise,30)