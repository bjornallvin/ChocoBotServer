import sys
import threading
import time
import DobotDllType as dType
import config as cfg

#api = dType.load()


# def GetPoseTask():
#    pos = dType.GetPose(api)
#    threading.Timer(0.2, GetPoseTask).start()


#threading.Timer(0.5, GetPoseTask).start()

# errorString = [
#    'Success',
#    'NotFound',
#    'Occupied']

#result = dType.ConnectDobot(api, "", 115200)
#print("Connect status:", errorString[result[0]])


class RobotArm:

    def __init__(self, ctx=None):

        super().__init__()

        self.ctx = ctx
        if self.ctx is not None:
            self.ctx.setRobotArm(self)
            # self.ctx.robotArmChanged.emit()

        # String describing Dobot robot arm connection status
        self.DOBOT_CON_STR = {
            dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
            dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
            dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

        self.connected = False
        self.lastIndex = 0
        self.initDobot()
        self.calibrated = False

        self.robotArmStandby = True

    def initDobot(self):

        ############################################################
        # load dynamic libraries and connect with the robot arm    #
        # you do not need to worry about this :D                   #
                                                                   #
        #Load Dll                                                  #
        self.dobotApi = dType.load()                               #
        #
        #Connect Dobot                                             #
        state = dType.ConnectDobot(self.dobotApi, "", 115200)[0]   #
        print("Connect status:", self.DOBOT_CON_STR[state])         #

        if state != 0:
            return 1
        self.connected = True
        #
        ############################################################

        print("clearing commnad queue")
        dType.SetQueuedCmdClear(self.dobotApi)
        dType.SetHOMEParams(self.dobotApi, 250, 0, 50, 0, isQueued=1)
        dType.SetPTPJointParams(self.dobotApi, 200, 200, 200, 200,
                                200, 200, 200, 200, isQueued=1)
        dType.SetPTPCommonParams(self.dobotApi, 50, 50, isQueued=1)

        # Start to Execute Command Queued
        dType.SetQueuedCmdStartExec(self.dobotApi)

    def test(self):
        print("Testing2...")
        dType.SetJOGCmd(self.dobotApi, 1, 1)
        time.sleep(0.5)
        dType.SetJOGCmd(self.dobotApi, 1, 0)
        time.sleep(1)
        dType.SetJOGCmd(self.dobotApi, 1, 2)
        time.sleep(0.5)
        dType.SetJOGCmd(self.dobotApi, 1, 0)
        # time.sleep(1)
        #dType.SetEndEffectorSuctionCup(self.dobotApi, 1, 1, isQueued=1)[0]
        # time.sleep(4)
        #dType.SetEndEffectorSuctionCup(self.dobotApi, 0, 1, isQueued=1)[0]
        # dType.DisconnectDobot(self.dobotApi)

    def homeRobotArm(self, ctx=None):
        if not self.connected:
            return 1
        if not self.robotArmStandby:
            return 1
        self.robotArmStandby = False

        self.stopClearRestartNow()
        # Async Home
        dType.SetHOMECmd(self.dobotApi, temp=0, isQueued=1)

        self.robotArmStandby = True

    # pick 1 chocolate accroding to the given index
    def pick1Choco(self, row, col, ctx=None):
        if not self.connected:
            return 1
        if not self.robotArmStandby:
            return 1
        self.robotArmStandby = False

        if ctx is None:
            ctx = self.ctx

        x, y = ctx.chocoHeartBox[(row, col)].locCoor
        x, y = self.boxToRoboCoor(x, y)

        dType.SetPTPCmd(self.dobotApi, dType.PTPMode.PTPMOVLXYZMode,
                        x, y, ctx.DOBOT_CUPUP, 0, isQueued=1)[0]
        dType.SetPTPCmd(self.dobotApi, dType.PTPMode.PTPMOVLXYZMode,
                        x, y, ctx.DOBOT_CUPDWN, 0, isQueued=1)[0]

        dType.SetEndEffectorSuctionCup(self.dobotApi, 1, 1, isQueued=1)[0]

        # the unit is seconds, somehow different from the documentation...
        dType.SetWAITCmd(self.dobotApi, 0.2, isQueued=1)
        # time.sleep(0.5)

        dType.SetPTPCmd(self.dobotApi, dType.PTPMode.PTPMOVLXYZMode,
                        x, y, ctx.DOBOT_CUPUP, 0, isQueued=1)[0]

        dType.SetPTPCmd(self.dobotApi, dType.PTPMode.PTPMOVLXYZMode,
                        ctx.dropCoor[0], ctx.dropCoor[1], ctx.dropCoor[2], 0, isQueued=1)[0]

        dType.SetEndEffectorSuctionCup(self.dobotApi, 0, 1, isQueued=1)[0]

        # dType.SetPTPCmd(self.dobotApi, dType.PTPMode.PTPMOVLXYZMode,
        #                x, y, ctx.DOBOT_CUPUP, 0, isQueued=1)[0]

        dType.SetPTPCmd(self.dobotApi, dType.PTPMode.PTPMOVLXYZMode,
                        ctx.standbyCoor[0], ctx.standbyCoor[1], ctx.standbyCoor[2], 0, isQueued=1)

        self.waitUntilQueueFinish()
        self.robotArmStandby = True

    # move to the position then pick and immediately drop
    def testPos(self, row, col, ctx=None):
        if not self.connected:
            return 1
        if not self.robotArmStandby:
            return 1
        self.robotArmStandby = False

        if ctx is None:
            ctx = self.ctx

        idx = (row, col)
        # self.stopClearRestartNow()

        print("testing pick and place at position {}".format(idx))
        x, y = ctx.chocoHeartBox[idx].locCoor
        x, y = self.boxToRoboCoor(x, y)

        dType.SetPTPCmd(self.dobotApi, dType.PTPMode.PTPMOVLXYZMode,
                        x, y, ctx.DOBOT_CUPUP, 0, isQueued=1)

        dType.SetPTPCmd(self.dobotApi, dType.PTPMode.PTPMOVLXYZMode,
                        x, y, ctx.DOBOT_CUPDWN, 0, isQueued=1)

        dType.SetEndEffectorSuctionCup(self.dobotApi, 1, 1, isQueued=1)

        # the docs said the time is in ms but apparently it is actually in sec
        dType.SetWAITCmd(self.dobotApi, 0.2, isQueued=1)

        dType.SetPTPCmd(self.dobotApi, dType.PTPMode.PTPMOVLXYZMode,
                        x, y, ctx.DOBOT_CUPUP-15, 0, isQueued=1)

        dType.SetPTPCmd(self.dobotApi, dType.PTPMode.PTPMOVLXYZMode,
                        x, y, ctx.DOBOT_CUPDWN + 5, 0, isQueued=1)

        dType.SetEndEffectorSuctionCup(self.dobotApi, 0, 1, isQueued=1)

        dType.SetPTPCmd(self.dobotApi, dType.PTPMode.PTPMOVLXYZMode,
                        x, y, ctx.DOBOT_CUPUP-15, 0, isQueued=1)

        self.waitUntilQueueFinish()
        self.robotArmStandby = True

    # move to the position and stay up
    def hoverToPos(self, x, y, ctx=None):
        if not self.connected:
            return 1
        if not self.robotArmStandby:
            return 1
        self.robotArmStandby = False

        if ctx is None:
            ctx = self.ctx

        self.stopClearRestartNow()

        print("Hover to position: {},{}".format(x, y))

        self.lastIndex = \
            dType.SetPTPCmd(self.dobotApi, dType.PTPMode.PTPMOVLXYZMode,
                            x, y, ctx.DOBOT_CUPUP, 0, isQueued=1)[0]

        self.robotArmStandby = True

    # disconnect from the robot arm
    def disconnect(self):
        if not self.connected:
            return 1

        self.stopClearNow()
        dType.DisconnectDobot(self.dobotApi)

    # stop the robot arm immediately and clear the queue
    def stopClearNow(self):
        if not self.connected:
            return 1

        dType.SetQueuedCmdForceStopExec(self.dobotApi)
        dType.SetEndEffectorSuctionCup(self.dobotApi, 0, 1, isQueued=0)[0]
        dType.SetQueuedCmdClear(self.dobotApi)

    # stop the robot arm immediately and clear the queue
    # then restart the queue
    def stopClearRestartNow(self):
        if not self.connected:
            return 1

        dType.SetQueuedCmdForceStopExec(self.dobotApi)
        dType.SetEndEffectorSuctionCup(self.dobotApi, 0, 1, isQueued=0)[0]
        dType.SetQueuedCmdClear(self.dobotApi)
        dType.SetQueuedCmdStartExec(self.dobotApi)

    # block programme flows until all queued actions are completed
    def waitUntilQueueFinish(self):
        if not self.connected:
            return 1

        # Wait for Executing Last Command
        while self.lastIndex > dType.GetQueuedCmdCurrentIndex(self.dobotApi)[0]:
            # blocking wait on the programing level only,
            # so the robot still execute the queued actions
            # while sleeping. unit: ms
            dType.dSleep(15)

    # map box coordinate to robot arm coordinate
    # this is just a reference to the function set in cfg file

    def boxToRoboCoor(self, x_box, y_box, ctx=None):
        return cfg.boxToRoboCoor(self, x_box, y_box, ctx=ctx)
