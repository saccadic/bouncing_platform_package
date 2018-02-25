#!/usr/bin/env python

import params as P
from PIDcontroller import PIDControl
from geometry_msgs.msg import Point
import rospy

class platformController:

    def __init__(self):
        self.xCtrl = PIDControl(P.kp, P.kd, P.theta_max, P.beta, P.Ts)
        self.yCtrl = PIDControl(P.kp, P.kd, P.phi_max, P.beta, P.Ts)
        self.sub = rospy.Subscriber('ball_position', Point, self.position_callback)
        self.ctrl_pub = rospy.Publisher('/controls', Platform_controls, queue_size=1)
        self.ref_sub = rospy.Subscriber('reference_position', Point, self.ref_callback)

    def u(self, ref, state):
        # ref is the input
        # state is the current state

        x_r = ref[0]
        x = state[0]
        y_r = ref[1]
        y = state[1]

        theta = self.xCtrl.PD(x_r, x, flag=False)
        phi = self.yCtrl.PD(y_r, y, flag=False)

        return [theta, phi]

    def position_callback(self, pt):

        x = pt.x
        y = pt.y
        state = [x,y]

        ref = [0,0]

        ctrls = self.u(ref,state)

        self.ctrl_pub.publish(ctrls[0],ctrls[1])

    def ref_callback(self,ref):
        self.refx = ref.x
        self.refy = ref.y


if __name__ == '__main__':

    rospy.init_node('controller', anonymous=True)

    pc = platformController()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shutting Down")