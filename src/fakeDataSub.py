#!/usr/bin/env python

import rospy

from geometry_msgs.msg import Twist, Pose2D, PoseStamped
from std_msgs.msg import *
from move_base_msgs.msg import *
from actionlib_msgs.msg import *

def goalSub(msg):
    print 'new goal ',msg.pose.position.x
    return

def callEVsub(msg):
    print 'elevator is going to ',msg.data
    return

def checkSub(msg):
    print 'check elevator'
    return

def enterEVsub(msg):
    print 'enter elevator',msg.data
    return

def alightEVsub(msg):
    print 'alight elevator',msg.data
    return

def changeMap(msg):
    print msg.data
    return

def changeAmclMap(msg):
    print msg.data
    return

def hotelGoalCB(msg):
    print msg.data
    return

def doorOpen(msg):
    print 'door open'
    return

def doorClose(msg):
    print 'door close'
    return

if __name__=="__main__":
    rospy.init_node('fake_data_sub')

    rospy.Subscriber('/move_base_simple/goal', PoseStamped,goalSub)
    rospy.Subscriber('/callEV',Int16,callEVsub)
    rospy.Subscriber('/checkEV',Bool,checkSub)
    rospy.Subscriber('/enterEV',String,enterEVsub)
    rospy.Subscriber('/alightEV',String,alightEVsub)
    rospy.Subscriber('/map_server_nav/reload',String,changeMap)
    rospy.Subscriber('/map_server_amcl/reload',String,changeAmclMap)
    rospy.Subscriber('/hotelGoalCB',String,hotelGoalCB)
    rospy.Subscriber('/doorOpen',Bool,doorOpen)
    rospy.Subscriber('/doorClose',Bool,doorClose)

    rospy.spin()