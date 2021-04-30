import rtde_control
import rtde_receive

rtde_c = rtde_control.RTDEControlInterface("192.168.88.129")
#rtde_r = rtde_receive.RTDEReceiveInterface("192.168.88.129")

rtde_c.moveL([-0.140,-0.440, 0.200 , 3.14, 0, 0], 0.5, 0.3)

#print(actual_pose)