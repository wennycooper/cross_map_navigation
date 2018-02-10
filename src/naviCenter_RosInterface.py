#!/usr/bin/env python

import rospy
import rospkg
import sys
import time
import math
import tf
from geometry_msgs.msg import Twist, Pose2D, PoseStamped
from std_msgs.msg import *
from move_base_msgs.msg import *
from actionlib_msgs.msg import *
from geometry_msgs.msg import *

from NavigationCenter.NaviCenter import NaviCenter
from NavigationCenter.hotelGoals import GoalMsg

rospack = rospkg.RosPack()
packPath = rospack.get_path('elevator')
print packPath

naviCenter = NaviCenter(packPath)
hotelGoals = GoalMsg()


goalPub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size = 1)
goalCancel = rospy.Publisher('/move_base/cancel',GoalID,queue_size = 1)
callEVpub = rospy.Publisher('/callEV',Int16,queue_size=1)
checkEVpub = rospy.Publisher('/checkEV',Bool,queue_size=1)
enterEVpub = rospy.Publisher('/enterEV',String,queue_size=1)
alightEVpub = rospy.Publisher('/alightEV',String,queue_size=1)
changeNavMapPub = rospy.Publisher('/map_server_nav/reload',String, queue_size=1)
changeAmclMapPub = rospy.Publisher('/map_server_amcl/reload',String, queue_size=1)
initPosePub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=10)
hotelGoalCBpub = rospy.Publisher('/hotelGoalCB',String,queue_size=1)
hotelGoalReachPub = rospy.Publisher('/hotelGoalReach',String,queue_size=1)
hotelGoalReachPub2 = rospy.Publisher('/hotelGoalReached',Bool,queue_size=1)
doorOpenPub = rospy.Publisher('/doorOpen',Bool,queue_size=1)
doorClosePub = rospy.Publisher('/doorClose',Bool,queue_size=1)


def goalPublish(goal):
    global hotelGoals,goalPub
    rosGoal = hotelGoals.toGoal(goal)
    goalPub.publish(rosGoal)
    return

def goalCancelPub():
    global goalCancel
    goalCancel.publish()
    return

def naviResultCB(msg):
    global naviCenter
    naviCenter.GoalReachCB()
    return

def hotelGoal(msg):
    global naviCenter
    if msg.data != 'Lobby':
        roomNumber = msg.data[1:4]
    else:
        roomNumber = 'Lobby'
    print roomNumber
    naviCenter.getNaviGoal(roomNumber)
    return

def hotelGoalCB(msg):
    global hotelGoalCBpub
    hotelGoalCBpub.publish(msg)
    return

def emergentStop(msg):
    global naviCenter
    naviCenter.cleanRoute()
    goalCancelPub()

def callEV(floor):
    global callEVpub
    callEVpub.publish(floor)
    return

def elevatorCB(msg):
    global naviCenter
    naviCenter.elevatorCB()
    return

def checkEV():
    global checkEVpub
    checkEVpub.publish(True)
    return

def checkEVcb(msg):
    global naviCenter,doorOpenPub,doorClosePub
    if msg.data:
        doorOpenPub.publish(True)
    else:
        doorClosePub.publish(True)
    naviCenter.enterEVcheckCB(msg.data)
    return

def enterEV(floor):
    global enterEVpub
    enterEVpub.publish(floor)
    return

def enterEVcb(msg):
    global naviCenter,doorOpenPub,doorClosePub
    if msg.data:
        doorClosePub.publish(True)
    naviCenter.enterEVcallback(msg.data)
    return

def alightEV(floor):
    global alightEVpub,doorOpenPub
    doorOpenPub.publish(True)
    alightEVpub.publish(floor)
    return

def alightEVcb(msg):
    global naviCenter,doorClosePub
    if msg.data:
        doorClosePub.publish(True)
    naviCenter.alightEVcallback(msg.data)
    return

def changeMap(floor):
    global naviCenter, hotelGoals, changeNavMapPub, changeAmclMapPub, initPosePub, packPath
    # pubMsg = {1:'change to 1F',2:'change to 2F',3:'change to 3F',4:'change to 4F'}
    pubNavMsg = {1:packPath+'/map/map'+str(floor)+'_nav.yaml',
            2:packPath+'/map/map'+str(floor)+'_nav.yaml',
            3:packPath+'/map/map'+str(floor)+'_nav.yaml',
            4:packPath+'/map/map'+str(floor)+'_nav.yaml'}
    pubAmclMsg = {1:packPath+'/map/map'+str(floor)+'_nav.yaml',
            2:packPath+'/map/map'+str(floor)+'_amcl.yaml',
            3:packPath+'/map/map'+str(floor)+'_amcl.yaml',
            4:packPath+'/map/map'+str(floor)+'_amcl.yaml'}
    changeNavMapPub.publish(pubNavMsg[floor])
    changeAmclMapPub.publish(pubAmclMsg[floor])
    initPosePub.publish(hotelGoals.getInitPose(floor))
    return

def hotelGoalReach(position):
    global hotelGoalReachPub,hotelGoalReachPub2
    hotelGoalReachPub.publish(position)
    hotelGoalReachPub2.publish(True)
    return


    



if __name__ == '__main__':

    rospy.init_node('NaviCenter',anonymous = True)
    
    naviCenter.register(goalPublish,callEV,checkEV,enterEV,alightEV,changeMap,
                        hotelGoalCB,hotelGoalReach)

    rospy.Subscriber('move_base/result', MoveBaseActionResult, naviResultCB)
    rospy.Subscriber('/hotelGoal', String, hotelGoal)
    rospy.Subscriber('/elevatorCB',Bool,elevatorCB)
    rospy.Subscriber('/checkEVcb',Bool,checkEVcb)
    rospy.Subscriber('/enterEVcb',Bool,enterEVcb)
    rospy.Subscriber('/alightEVcb',Bool,alightEVcb)
    rospy.Subscriber('/emergentStop',Bool,emergentStop)

    time.sleep(1)
    changeNavMapPub.publish(packPath+'/map/map1_nav.yaml')
    changeAmclMapPub.publish(packPath+'/map/map1_amcl.yaml')
    initPosePub.publish(hotelGoals.startPose())

    rospy.spin()