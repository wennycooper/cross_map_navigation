

class RobotStatus:

    def __init__(self):
        self.status = 'init'
        self.position = ''

    def isAvailable(self):
        if self.status == 'available':
            return True
        else:
            return False

    def isWaitEV(self):
        if self.status == 'waitEV':
            return True
        else:
            return False

    def isInEV(self):
        if self.status == 'inEV':
            return True
        else:
            return False

    def setAvailable(self):
        self.status = 'available'

    def setMoving(self):
        self.status = 'moving'

    def setWaitEV(self):
        self.status = 'waitEV'

    def setInEV(self):
        self.status = 'inEV'

    def getPosition(self):
        return self.position

    def setPosition(self,newPose):
        self.position = newPose