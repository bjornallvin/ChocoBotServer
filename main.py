import time
from http.server import HTTPServer
from server import Server
from RobotArmHandling import RobotArm
import helper

HOST_NAME = ''
PORT_NUMBER = 8000

if __name__ == '__main__':

    helper.ctx = helper.AppContext()
    helper.ctx.setRobotArm(RobotArm(helper.ctx))

    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
