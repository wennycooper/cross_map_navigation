from geometry_msgs.msg import *
from move_base_msgs.msg import *

class GoalMsg:

    def __init__(self):
        print 'goals inited'

    def toGoal(self,goal):
        goalDic = {'Lobby':self.toLobby,
                    'EVW1':self.toEVW1,'EVW2':self.toEVW2,'EVW3':self.toEVW3,'EVW4':self.toEVW4,
                    '201':self.to201,'202':self.to202,'203':self.to203,
                    '301':self.to301,'302':self.to302,'303':self.to303,
                    '401':self.to401,'402':self.to402,'403':self.to403}
        rosGoal = goalDic[goal]()
        return rosGoal

    def getInitPose(self,floor):
        poseDic = {1:self.EVin1,2:self.EVin2,3:self.EVin3,4:self.EVin4}
        pose = poseDic[floor]()
        return pose

    def getELlist(self):
        ELlist = ['EVW1','EVW2','EVW3','EVW4']
        return ELlist

    def toLobby(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = 13.35
        goal.pose.position.y = 13.85
        goal.pose.orientation.z = -0.7
        goal.pose.orientation.w = 0.7
        return goal

    def toEVW1(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = 14.4
        goal.pose.position.y = 19.55
        goal.pose.orientation.z = 1
        goal.pose.orientation.w = 0
        return goal

    def toEVW2(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = 14.4
        goal.pose.position.y = 19.55
        goal.pose.orientation.z = 1
        goal.pose.orientation.w = 0
        return goal

    def toEVW3(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = 14.4
        goal.pose.position.y = 19.55
        goal.pose.orientation.z = 1
        goal.pose.orientation.w = 0
        return goal

    def toEVW4(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = 14.4
        goal.pose.position.y = 19.55
        goal.pose.orientation.z = 1
        goal.pose.orientation.w = 0
        return goal

    def to201(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = 17.13
        goal.pose.position.y = 15.92
        goal.pose.orientation.z = 1
        return goal

    def to202(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = 13.35
        goal.pose.position.y = 13.85
        goal.pose.orientation.z = -0.7
        goal.pose.orientation.w = 0.7
        return goal

    def to203(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = 13.56
        goal.pose.position.y = 8.57
        goal.pose.orientation.w = 1
        return goal

    def to301(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = 17.13
        goal.pose.position.y = 15.92
        goal.pose.orientation.z = 1
        return goal

    def to302(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = 13.35
        goal.pose.position.y = 13.85
        goal.pose.orientation.z = -0.7
        goal.pose.orientation.w = 0.7
        return goal

    def to303(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = 13.56
        goal.pose.position.y = 8.57
        goal.pose.orientation.w = 1
        return goal

    def to401(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = 17.13
        goal.pose.position.y = 15.92
        goal.pose.orientation.z = 1
        return goal

    def to402(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = 13.35
        goal.pose.position.y = 13.85
        goal.pose.orientation.z = -0.7
        goal.pose.orientation.w = 0.7
        return goal

    def to403(self):
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = 13.56
        goal.pose.position.y = 8.57
        goal.pose.orientation.w = 1
        return goal


    def EVin1(self):
        initPose = PoseWithCovarianceStamped()
        initPose.header.frame_id = 'map'
        initPose.pose.pose.position.x = 16.74
        initPose.pose.pose.position.y = 19.44
        initPose.pose.pose.orientation.z = 1
        initPose.pose.covariance[0] = 0.25
        initPose.pose.covariance[7] = 0.25
        initPose.pose.covariance[35] = 0.066
        return initPose

    def EVin2(self):
        initPose = PoseWithCovarianceStamped()
        initPose.header.frame_id = 'map'
        initPose.pose.pose.position.x = 16.74
        initPose.pose.pose.position.y = 19.44
        initPose.pose.pose.orientation.z = 1
        initPose.pose.covariance[0] = 0.25
        initPose.pose.covariance[7] = 0.25
        initPose.pose.covariance[35] = 0.066
        return initPose

    def EVin3(self):
        initPose = PoseWithCovarianceStamped()
        initPose.header.frame_id = 'map'
        initPose.pose.pose.position.x = 16.74
        initPose.pose.pose.position.y = 19.44
        initPose.pose.pose.orientation.z = 1
        initPose.pose.covariance[0] = 0.25
        initPose.pose.covariance[7] = 0.25
        initPose.pose.covariance[35] = 0.066
        return initPose

    def EVin4(self):
        initPose = PoseWithCovarianceStamped()
        initPose.header.frame_id = 'map'
        initPose.pose.pose.position.x = 16.74
        initPose.pose.pose.position.y = 19.44
        initPose.pose.pose.orientation.z = 1
        initPose.pose.covariance[0] = 0.25
        initPose.pose.covariance[7] = 0.25
        initPose.pose.covariance[35] = 0.066
        return initPose

    def startPose(self):
        initPose = PoseWithCovarianceStamped()
        initPose.header.frame_id = 'map'
        initPose.pose.pose.position.x = 13.35
        initPose.pose.pose.position.y = 13.85
        initPose.pose.pose.orientation.z = -0.7
        initPose.pose.pose.orientation.w = 0.7
        initPose.pose.covariance[0] = 0.25
        initPose.pose.covariance[7] = 0.25
        initPose.pose.covariance[35] = 0.066
        return initPose