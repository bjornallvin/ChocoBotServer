#!/usr/bin/env python3
"""Handle api for robot

"""
from http.server import BaseHTTPRequestHandler
import helper
import json


class Server(BaseHTTPRequestHandler):
    """ Server to handle http request

    """

    def do_HEAD(self):
        return

    def do_GET(self):

        self.robotArm = helper.ctx.getRobotArm()

        pathList = self.path.split("/")
        if (len(pathList) < 2 or len(pathList) > 3):
            self.send_json_response(
                {'result': 'ERROR-UNKNOWN', 'message': 'Unknown command'})
            return

        cmd = pathList[1]
        validCmds = ["pick", "home", "test", "refill", "connect"]
        if cmd not in validCmds:
            self.send_json_response(
                {'result': 'ERROR-UNKNOWN', 'message': 'Unknown command'})
            return

        cmdArg = None
        if len(pathList) > 2:
            cmdArg = pathList[2]

        # ----------------------------------------------------------
        #
        #   Connect
        #
        # ----------------------------------------------------------
        if cmd == "connect":
            if self.robotArm.connected == True:
                self.send_json_response(
                    {'result': 'ERROR-CONNECTED', 'message': 'Robot arm allready connected'})
            else:
                self.robotArm.initDobot()
                if self.robotArm.connected == True:
                    self.send_json_response(
                        {'result': 'SUCCESS', 'message': 'Robot arm was connected'})
                else:
                    self.send_json_response(
                        {'result': 'ERROR-DISCONNECTED', 'message': 'Robot arm could not be connected'})

        elif cmd == "pick":
            self.pick(cmdArg)

        elif cmd == "test":
            self.test(cmdArg)

        elif cmd == "home":
            self.home()

        elif cmd == "refill":
            self.refill()

        else:
            self.send_json_response(
                {'result': 'ERROR-UNKNOWN', 'message': 'Unknown command'})

    def do_POST(self):
        return

    def pick(self, slot=None):
        if self.robotArm.connected == False:
            self.send_json_response(
                {'result': 'ERROR-DISCONNECTED', 'message': 'Robot arm disconnected'})
            return

        if slot is not None:
            """pick specific slot"""
            self.robotArm.pick1ChocoByIndex(int(slot))
            message = 'Picked nr ' + str(slot)
            self.send_json_response(
                {'result': 'SUCCESS', 'message': message})

        else:

            chocosLeft = helper.ctx.getChocosLeft()
            chocosTotal = helper.ctx.getChocoNum()

            if chocosLeft > 0:
                chocoToPick = chocosTotal - chocosLeft + 1
                self.robotArm.pick1ChocoByIndex(int(chocoToPick))

                helper.ctx.setChocosLeft(chocosLeft - 1)
                message = 'Picked nr ' + str(chocoToPick)
                self.send_json_response(
                    {'result': 'SUCCESS', 'message': message})
            else:
                self.send_json_response(
                    {'result': 'ERROR-EMPTY', 'message': 'Out of chocos. Please refill'})

    def test(self, slot="all"):
        if self.robotArm.connected == False:
            self.send_json_response(
                {'result': 'ERROR-DISCONNECTED', 'message': 'Robot arm disconnected'})
            return

        if (slot == "all"):
            for i in range(11):
                self.robotArm.testPosByIndex(int(i+1))
        else:
            self.robotArm.testPosByIndex(int(slot))

        self.send_json_response(
            {'result': 'SUCCESS', 'message': 'Testing done'})

    def refill(self):
        """Called after robot candy refilled
        """
        if self.robotArm.connected == False:
            self.send_json_response(
                {'result': 'ERROR-DISCONNECTED', 'message': 'Robot arm disconnected'})
            return
        helper.ctx.setChocosLeft(helper.ctx.getChocoNum())
        self.send_json_response(
            {'result': 'SUCCESS', 'message': 'Refilled ok'})

    def home(self):
        if self.robotArm.connected == False:
            self.send_json_response(
                {'result': 'ERROR-DISCONNECTED', 'message': 'Robot arm disconnected'})
            return
        self.robotArm.homeRobotArm()
        self.send_json_response(
            {'result': 'SUCCESS', 'message': 'Robot arm position reset'})

    def send_json_response(self, json_object):
        """Send json back to the browser
        """
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(
            bytes(json.dumps(json_object, ensure_ascii=False), 'utf-8'))
