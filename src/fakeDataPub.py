#!/usr/bin/env python

import rospy

from geometry_msgs.msg import Twist, Pose2D, PoseStamped
from std_msgs.msg import *
from move_base_msgs.msg import *
from actionlib_msgs.msg import *

import sys, select, termios, tty


goalReachedPub = rospy.Publisher('/move_base/result', MoveBaseActionResult,queue_size=1)
elevatorReachedPub = rospy.Publisher('/elevatorCB',Bool,queue_size=1)
checkPub = rospy.Publisher('/checkEVcb',Bool,queue_size=1)
enterEVpub = rospy.Publisher('/enterEVcb',Bool,queue_size=1)
alightEVpub = rospy.Publisher('/alightEVcb',Bool,queue_size=1)

def goalReached():
    global goalReachedPub
    msg = MoveBaseActionResult()
    msg.status.status = 3
    goalReachedPub.publish(msg)
    return

def elevatorReached():
    global elevatorReachedPub
    msg = Bool()
    msg.data = True
    elevatorReachedPub.publish(msg)
    return

def checkResponse():
    global checkPub
    msg = Bool()
    msg.data = True
    checkPub.publish(msg)
    return

def enterResponse():
    global enterEVpub
    msg = Bool()
    msg.data = True
    enterEVpub.publish(msg)
    return

def alightResponse():
    global alightEVpub
    msg = Bool()
    msg.data = True
    alightEVpub.publish(msg)
    return

pubBindings = {
    '1':goalReached,
    '2':elevatorReached,
    '3':checkResponse,
    '4':enterResponse,
    '5':alightResponse
}

msg = """
1:goalReached
2:elevatorReached
3:checkResponse
4:enterResponse
5:alightResponse
"""

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('fake_data')

    try:
        print msg
        while(1):
            key = getKey()
            if key in pubBindings.keys():
                pubBindings[key]()
            else:
                if(key == '\x03'):
                    break


    except:
        print 'shit happens'


    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
