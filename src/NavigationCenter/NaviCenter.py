import time
import csv
import os
from threading import Timer
from NavigationCenter.RobotStatus import RobotStatus
from datetime import datetime
from collections import defaultdict
from heapq import *
from Queue import *



class NaviCenter:

    def __init__(self,naviFilePath):
        filePath = naviFilePath + '/src/NavigationCenter/navi_path.csv'
        pathfile = open(filePath,'rb')
        pathreader = csv.reader(pathfile,dialect = 'excel')

        self.pathDic = defaultdict(list)
        for l,r,c in pathreader:
            self.pathDic[l].append((int(c),r))
        
        print self.pathDic

        self.robotstatus = RobotStatus()
        self.goalList = []

        self.setPosition('Lobby')
        self.robotstatus.setAvailable()

    def register(self,pubGoalFunc,callEVFunc,evCheckFunc,enterEvFunc,
                alightEvFunc,changeMap,setGoalCBFunc,reachCBFunc):
        self.pubRosGoal = pubGoalFunc
        self.callEV = callEVFunc
        self.evCheck = evCheckFunc
        self.evEnter = enterEvFunc
        self.evAlight = alightEvFunc
        self.changeMap = changeMap
        self.setGoalCB = setGoalCBFunc
        self.reachCB = reachCBFunc

    def pubGoal(self,goal):
        self.pubRosGoal(goal)

    def goNextGoal(self):
        self.robotstatus.setMoving()
        goal = self.goalList[0]
        print 'Next Goal', goal
        self.pubGoal(goal)
        return
        
    def hasNextGoal(self):
        if self.goalList != []:
            return True
        else:
            return False

    def GoalReachCB(self):
        if self.hasNextGoal():
            self.setPosition(self.goalList.pop(0))
            print 'reach ',self.robotstatus.getPosition()
        else:
            self.naviGoalReached()

        if self.hasNextGoal():
            if self.goalList[0] == 'EVin':
                self.robotstatus.setWaitEV()
                self.callElevator(self.robotstatus.getPosition())
            else:
                self.goNextGoal()
        else:
            self.naviGoalReached()
        return

    def setPosition(self,position):
        self.robotstatus.setPosition(position)

    def getNaviGoal(self,goal):
        if self.robotstatus.isAvailable():
            if self.setRoute(goal):
                self.goNextGoal()
            else:
                return  
        else:
            print 'robot is busy'
            self.setGoalCB('busy')
            return

    def naviGoalReached(self):
        print 'navi goal reached'
        self.robotstatus.setAvailable()
        self.reachCB(self.robotstatus.getPosition())
        return
                

    def setRoute(self,destination):
        path = self.calculatePath(self.robotstatus.position,destination)
        if path != None:
            for stop in path:
                self.goalList.append(stop)
            self.setGoalCB('success')
            return True
        else:
            print 'plane failed'
            self.setGoalCB('error')
            return False
       
        
    def cleanRoute(self):
        self.goalList = []

    def calculatePath(self,start,destination):
        print 'dijkstra ',start,destination
        try:
            (cost,path) = self.dijkstra(self.pathDic,start,destination)
            print 'cost = ',cost
            print 'path = ',path
        except:
            print 'path error'
            return None
        
        return path

    def dijkstra(self,pathdic, f, t):
        pathBuf = list()
        q, seen = [(0,f,pathBuf)], set()
        while q:
            (cost,v1,path) = heappop(q)
            if v1 not in seen:
                seen.add(v1)
                path.append(v1)
                if v1 == t: return (cost, path)

                for c, v2 in pathdic.get(v1, ()):
                    if v2 not in seen:
                        path2 = path[0:]
                        heappush(q, (cost+c, v2, path2))
                        path2 = []

        return float("inf")

    def callElevator(self,destination):
        EVdic = {'EVW1':1,'EVW2':2,'EVW3':3,'EVW4':4}
        print 'call elevator to ',EVdic[destination]
        self.callEV(EVdic[destination])
        return

    def elevatorCB(self):
        print 'robot status',self.robotstatus.status
        if self.robotstatus.isWaitEV():
            self.enterEVcheck()
        elif self.robotstatus.isInEV():
            t = Timer(3,self.alightEV)
            t.daemon = True
            t.start()
            # self.alightEV()
        else:
            print 'elevator callback error'
        return

    def enterEVcheck(self):
        print 'checking elevator'
        self.evCheck()
        return

    def enterEVcheckCB(self,available):
        if available:
            print 'elevator is available'
            self.enterEV()
        else:
            print 'wait for next one'
            evGoal = self.robotstatus.getPosition()
            t = Timer(3,self.callElevator,[evGoal])
            t.daemon = True
            t.start()
        return

    def enterEV(self):
        EVdic = {'EVW1':'1F','EVW2':'2F','EVW3':'3F','EVW4':'4F'}
        self.evEnter(EVdic[self.robotstatus.getPosition()])
        print 'entering elevator'
        return

    def enterEVcallback(self,success):
        if success:
            position = self.goalList.pop(0)
            self.robotstatus.setPosition(position)
            self.robotstatus.setInEV()
            self.callElevator(self.goalList[0])
            self.changeNaviMap(self.goalList[0])
            print 'in the elevator'
        else:
            print 'enter elevator failed'
        return

    def alightEV(self):
        EVdic = {'EVW1':'1F','EVW2':'2F','EVW3':'3F','EVW4':'4F'}
        self.evAlight(EVdic[self.goalList[0]])
        print 'alighting elevator'
        return

    def alightEVcallback(self,success):
        if success:
            position = self.goalList.pop(0)
            self.robotstatus.setPosition(position)
            self.robotstatus.setMoving()
            print 'reach ',self.robotstatus.getPosition()
            if self.hasNextGoal():
                self.goNextGoal()
                return
            else:
                self.naviGoalReached()
                
        return

    def changeNaviMap(self,destination):
        EVdic = {'EVW1':1,'EVW2':2,'EVW3':3,'EVW4':4}
        print 'change map to ',EVdic[destination]
        self.changeMap(EVdic[destination])
        return

    