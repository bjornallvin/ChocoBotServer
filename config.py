# python script used as config file
# may not be a secure practice but in our case
# it get the job done faster and the applicaion has
# no open internet connection so probably fine


# total number of chocolate
chocoNum = 11

# z-level for down, calibration, and up position
DOBOT_CUPDWN = -27
DOBOT_CUPCAL = -21
DOBOT_CUPUP = +20

# chocolate dropping location in robot coordinate
dropCoor = [150, 115, 50]

standbyCoor = [210, 0, 40]

# offset for the origin
# usually use as the starting point/coordinate
# of the first chocolate position (in robot coordinate)
#
# actually usage always depends on how the boxToRoboCoor
# function is defined
DOBOT_OFFSET_X = 210
DOBOT_OFFSET_Y = 45

# map box coordinate to robot coordinate


def boxToRoboCoor(self, x_box, y_box, ctx=None):
    if ctx is None:
        ctx = self.ctx

    x_robo = -x_box + ctx.DOBOT_OFFSET_X
    y_robo = -y_box + ctx.DOBOT_OFFSET_Y
    return x_robo, y_robo


# define the location of every chocolate
# in the box relative to the orgin defined by
# the offset: DOBOT_OFFSET_X, DOBOT_OFFSET_Y
chocoHeartBoxGrid = {
    (0, 0): (0, 0),

    (1, 0): (-23.7, +19.4),
    (1, 1): (+27, +18),

    (2, 0): (-41.5, +52),
    (2, 1): (-7.8, +63),
    (2, 2): (+17.3, +50),
    (2, 3): (+48.5, +48),

    (3, 0): (-43.0, +87),
    (3, 1): (-15.0, +101.0),
    (3, 2): (+24.0, +100.0),
    (3, 3): (+53.6, +82),
}
