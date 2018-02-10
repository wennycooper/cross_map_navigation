#!/usr/bin/env python

import cherrypy
import requests

import rospy
import sys
import time
from std_msgs.msg import *

s = requests.Session()
elevatorIP = 'http://192.168.2.101:8080/'
phoneServerIP = 'http://192.168.25.210:8080/'
password = ''

class PC_server(object):
    elevatorReachedPub = rospy.Publisher('/elevatorCB',Bool,queue_size=1)

    @cherrypy.expose
    def index(self):
        return "Hello world!"
    
    @cherrypy.expose
    def reached(self):
        print 'elevator reach'
        self.elevatorReachedPub.publish(True)
        return "GOOOOOOOOOOOOD!"
    
    @cherrypy.expose
    def shutdown(self):  
        cherrypy.engine.exit()


def doorOpen(msg):
    print 'door open'
    time.sleep(0.5)
    r = s.get(elevatorIP + 'open')
    time.sleep(0.5)
    return

def doorClose(msg):
    print 'door close'
    time.sleep(0.5)
    r = s.get(elevatorIP + 'close')
    time.sleep(0.5)
    return

def callElevator(msg):
    print 'call elevator to ',msg.data
    time.sleep(0.5)
    r = s.get(elevatorIP + 'call?floor=' + str(msg.data))
    time.sleep(0.5)
    return

def updatePW(msg):
    global password
    password = msg.data
    return


def goalReachCB(msg):
    global password
    print 'hotel goal reached ',msg.data
    time.sleep(0.5)
    
    # r = s.get(phoneServerIP + 'robocall?roomId=15&pw=1234')
    if password != '':
        # r = s.get(phoneServerIP + 'robocall?roomId=' + msg.data + '&pw=' + password)
        r = s.get(phoneServerIP + 'robocall?roomId=15&pw=' + password)
        time.sleep(0.5)
    else:
        print 'No password'
    password = ''

    return


if __name__ == '__main__':
    rospy.init_node('NaviCenter',anonymous = False)
    rospy.Subscriber('/doorOpen',Bool,doorOpen)
    rospy.Subscriber('/doorClose',Bool,doorClose)
    rospy.Subscriber('/callEV',Int16,callElevator)
    rospy.Subscriber('/hotelGoalReach',String,goalReachCB)
    rospy.Subscriber('/pw',String,updatePW)
    # rospy.spin()

    # if rospy.is_shutdown:
    #     print 'ros node dead'

    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.socket_port = 7070
    cherrypy.server.thread_pool = 10
    cherrypy.quickstart(PC_server())
