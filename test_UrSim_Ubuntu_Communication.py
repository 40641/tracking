import rtde_control
import rtde_receive

rtde_c = rtde_control.RTDEControlInterface("192.168.88.129")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.88.129")
actual_tcp_pose = rtde_r.getActualTCPPose()

new_z = actual_tcp_pose[2]+0.050

rtde_c.moveL([-0.140,-0.440, new_z , 3.14, 0, 0], 0.5, 0.3)
actual_tcp_pose = rtde_r.getActualTCPPose()


print(actual_tcp_pose)
