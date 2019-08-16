# def init():
import logging
import config as cfg
global ctx


#from PySide2.QtCore import QObject, Signal, Slot, Property

DEBUG = logging.debug
INFO = logging.info
WARN = logging.warning
ERR = logging.error
CRIT = logging.critical
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)


class ChocoHeartBox(dict):
    # def initChocoHeartBox():
    def __init__(self, chocoHeartBoxGrid):
        print("initiating chocoHeartBox")
        for key, value in chocoHeartBoxGrid.items():
            self[key] = ChocoHeartSlot(*value)
            self[key].box = self
            print("added slot at loc: {}, {}".format(*value))


class ChocoHeartSlot():
    def __init__(self, x_coor=0, y_coor=0):
        self.isEmpty = False
        self.isFilling = False
        self.locCoor = (x_coor, y_coor)


class AppContext():
    def __init__(self):
        super().__init__()

        self.chocoHeartBoxGrid = cfg.chocoHeartBoxGrid

        self.chocoHeartBox = ChocoHeartBox(cfg.chocoHeartBoxGrid)

        self.__chocoNum = cfg.chocoNum
        self.__chocosLeft = cfg.chocoNum

        self.__robotArm = None
        self.__giveChoco = False

        self.dropCoor = cfg.dropCoor
        self.standbyCoor = cfg.standbyCoor

        self.DOBOT_OFFSET_X = cfg.DOBOT_OFFSET_X
        self.DOBOT_OFFSET_Y = cfg.DOBOT_OFFSET_Y

        self.__DOBOT_CUPDWN = cfg.DOBOT_CUPDWN
        self.DOBOT_CUPDWN = cfg.DOBOT_CUPDWN
        self.__DOBOT_CUPCAL = cfg.DOBOT_CUPCAL
        self.DOBOT_CUPUP = cfg.DOBOT_CUPUP

    def getChocosLeft(self):
        return self.__chocosLeft

    def setChocosLeft(self, chocosLeft):
        self.__chocosLeft = chocosLeft

    def resetChocosLeft(self):
        self.__chocosLeft = __chocoNum

    def getChocoNum(self):
        return self.__chocoNum

    def setChocoNum(self, chocoNum):
        self.__chocoNum = chocoNum

   # chocoNum = Property(int, getChocoNum, setChocoNum, notify=chocoNumChanged)

    # define the QProperty DOBOT_CUPDWN, which get and set "__DOBOT_CUPDWN"

    def getDOBOT_CUPDWN(self):
        return self.__DOBOT_CUPDWN

    def setDOBOT_CUPDWN(self, dobot_cupdwn):
        self.__DOBOT_CUPDWN = dobot_cupdwn

    # define the QProperty DOBOT_CUPCAL, which get and set "__DOBOT_CUPCAL"

    def getDOBOT_CUPCAL(self):
        return self.__DOBOT_CUPCAL

    def setDOBOT_CUPCAL(self, DOBOT_CUPCAL):
        self.__DOBOT_CUPCAL = DOBOT_CUPCAL

    # define the QProperty robotArm, which get and set "__robotArm"

    def getRobotArm(self):
        return self.__robotArm

    def setRobotArm(self, robotArm):
        self.__robotArm = robotArm

    def getGiveChoco(self):
        return self.__giveChoco

    def setGiveChoco(self, boolean):
        self.__giveChoco = boolean

    def getSlotCoor(self, row, col):
        DEBUG("getSlotCoor: {}".format(self.chocoHeartBox[(row, col)].locCoor))
        return self.chocoHeartBox[(row, col)].locCoor

    def getSlotCoorX(self, row, col):
        DEBUG("getSlotCoorX: {}".format(
            self.chocoHeartBox[(row, col)].locCoor[0]))
        return self.chocoHeartBox[(row, col)].locCoor[0]

    def getSlotCoorY(self, row, col):
        DEBUG("getSlotCoorY: {}".format(
            self.chocoHeartBox[(row, col)].locCoor[1]))
        return self.chocoHeartBox[(row, col)].locCoor[1]

    def setSlotCoor(self, row, col, x, y):
        DEBUG("setSlotCoor slot({},{}).locCoor-> {},{}".format(row, col, x, y))
        self.chocoHeartBox[(row, col)].locCoor = (x, y)

    def getDropCoor(self):
        DEBUG("getDropCoor: {}".format(self.dropCoor))
        return self.dropCoor

    def getDropCoorX(self):
        DEBUG("getDropCoorX: {}".format(self.dropCoor[0]))
        return self.dropCoor[0]

    def getDropCoorY(self):
        DEBUG("getDropCoorY: {}".format(self.dropCoor[1]))
        return self.dropCoor[1]

    def setDropCoor(self, x, y):
        DEBUG("setDropCoor: {},{}".format(x, y))
        self.dropCoor[0] = x
        self.dropCoor[1] = y
