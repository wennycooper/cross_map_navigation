#!/usr/bin/env python

from threading import Timer

import rospy
from geometry_msgs.msg import Twist, Pose2D, PoseStamped
from std_msgs.msg import *
from move_base_msgs.msg import *
from actionlib_msgs.msg import *
from apriltags_ros.msg import *

avalability = False
tagOne = False
tagTwo = False
checkCBPub = rospy.Publisher('/checkEVcb',Bool,queue_size=1)

def detectionCB(tagArray):
    global tagOne, tagTwo
    if len(tagArray.detections) != 0:
        for tag in tagArray.detections:
            if tag.id == 1:
                tagOne = True
                print 'tag one OK'
            elif tag.id == 2:
                tagTwo= True
                print 'tag two OK'
            else:
                pass
    else:
        return
    return

def chekc_elevator(msg):
    global tagOne, tagTwo
    tagOne = False
    tagTwo = False
    t = Timer(3,chekc_elevatorCB)
    t.daemon = True
    t.start()
    return

def chekc_elevatorCB():
    global tagOne, tagTwo, checkCBPub
    print str(tagOne),str(tagTwo)
    if tagOne and tagTwo:
        checkCBPub.publish(True)
    else:
        checkCBPub.publish(False)
    return    




if __name__=="__main__":
    rospy.init_node('elevator_checker')
    rospy.Subscriber('/camera_rear/tag_detections',AprilTagDetectionArray,detectionCB)
    rospy.Subscriber('/checkEV',Bool,chekc_elevator)

    rospy.spin()