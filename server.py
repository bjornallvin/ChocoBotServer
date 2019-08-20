from http.server import BaseHTTPRequestHandler
import helper
import json


class Server(BaseHTTPRequestHandler):

    def do_HEAD(self):
        return

    def do_GET(self):

        self.robotArm = helper.ctx.getRobotArm()

        # ----------------------------------------------------------
        #
        #   Connect
        #
        # ----------------------------------------------------------
        if self.path == "/connect":
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

        # ----------------------------------------------------------
        #
        #   Pick
        #
        # ----------------------------------------------------------
        elif self.path == "/pick":

            if self.robotArm.connected == False:
                self.send_json_response(
                    {'result': 'ERROR-DISCONNECTED', 'message': 'Robot arm disconnected'})
                return

            chocosLeft = helper.ctx.getChocosLeft()
            chocosTotal = helper.ctx.getChocoNum()

            if chocosLeft > 0:
                chocoToPick = chocosTotal - chocosLeft + 1
                if chocoToPick == 1:  # first choco
                    self.robotArm.pick1Choco(0, 0)
                elif chocoToPick == 2:
                    self.robotArm.pick1Choco(1, 0)
                elif chocoToPick == 3:
                    self.robotArm.pick1Choco(1, 1)
                elif chocoToPick == 4:
                    self.robotArm.pick1Choco(2, 0)
                elif chocoToPick == 5:
                    self.robotArm.pick1Choco(2, 1)
                elif chocoToPick == 6:
                    self.robotArm.pick1Choco(2, 2)
                elif chocoToPick == 7:
                    self.robotArm.pick1Choco(2, 3)
                elif chocoToPick == 8:
                    self.robotArm.pick1Choco(3, 0)
                elif chocoToPick == 9:
                    self.robotArm.pick1Choco(3, 1)
                elif chocoToPick == 10:
                    self.robotArm.pick1Choco(3, 2)
                elif chocoToPick == 11:
                    self.robotArm.pick1Choco(3, 3)

                helper.ctx.setChocosLeft(chocosLeft - 1)
                message = 'Picked nr ' + str(chocoToPick)
                self.send_json_response(
                    {'result': 'SUCCESS', 'message': message})
            else:
                self.send_json_response(
                    {'result': 'ERROR-EMPTY', 'message': 'Out of chocos. Please refill'})

        # ----------------------------------------------------------
        #
        #
        #
        # ----------------------------------------------------------
        elif self.path == "/pick/1":
            self.robotArm.pick1Choco(0, 0)
        elif self.path == "/pick/2":
            self.robotArm.pick1Choco(1, 0)
        elif self.path == "/pick/3":
            self.robotArm.pick1Choco(1, 1)
        elif self.path == "/pick/4":
            self.robotArm.pick1Choco(2, 0)
        elif self.path == "/pick/5":
            self.robotArm.pick1Choco(2, 1)
        elif self.path == "/pick/6":
            self.robotArm.pick1Choco(2, 2)
        elif self.path == "/pick/7":
            self.robotArm.pick1Choco(2, 3)
        elif self.path == "/pick/8":
            self.robotArm.pick1Choco(3, 0)
        elif self.path == "/pick/9":
            self.robotArm.pick1Choco(3, 1)
        elif self.path == "/pick/10":
            self.robotArm.pick1Choco(3, 2)
        elif self.path == "/pick/11":
            self.robotArm.pick1Choco(3, 3)

        # ----------------------------------------------------------
        #
        #
        #
        # ----------------------------------------------------------
        elif self.path == "/test/1":
            self.robotArm.testPos(0, 0)
        elif self.path == "/test/2":
            self.robotArm.testPos(1, 0)
        elif self.path == "/test/3":
            self.robotArm.testPos(1, 1)
        elif self.path == "/test/4":
            self.robotArm.testPos(2, 0)
        elif self.path == "/test/5":
            self.robotArm.testPos(2, 1)
        elif self.path == "/test/6":
            self.robotArm.testPos(2, 2)
        elif self.path == "/test/7":
            self.robotArm.testPos(2, 3)
        elif self.path == "/test/8":
            self.robotArm.testPos(3, 0)
        elif self.path == "/test/9":
            self.robotArm.testPos(3, 1)
        elif self.path == "/test/10":
            self.robotArm.testPos(3, 2)
        elif self.path == "/test/11":
            self.robotArm.testPos(3, 3)

        # ----------------------------------------------------------
        #
        #   Test
        #
        # ----------------------------------------------------------
        elif self.path == "/test/all":
            if self.robotArm.connected == False:
                self.send_json_response(
                    {'result': 'ERROR-DISCONNECTED', 'message': 'Robot arm disconnected'})
                return

            self.robotArm.testPos(0, 0)
            self.robotArm.testPos(1, 0)
            self.robotArm.testPos(1, 1)
            self.robotArm.testPos(2, 0)
            self.robotArm.testPos(2, 1)
            self.robotArm.testPos(2, 2)
            self.robotArm.testPos(2, 3)
            self.robotArm.testPos(3, 0)
            self.robotArm.testPos(3, 1)
            self.robotArm.testPos(3, 2)
            self.robotArm.testPos(3, 3)
            self.send_json_response(
                {'result': 'SUCCESS', 'message': 'Testing done'})

        # ----------------------------------------------------------
        #
        #
        #
        # ----------------------------------------------------------
        elif self.path == "/home":
            if self.robotArm.connected == False:
                self.send_json_response(
                    {'result': 'ERROR-DISCONNECTED', 'message': 'Robot arm disconnected'})
                return
            self.robotArm.homeRobotArm()
            self.send_json_response(
                {'result': 'SUCCESS', 'message': 'Robot arm position reset'})

        # ----------------------------------------------------------
        #
        #   Refill
        #
        # ----------------------------------------------------------
        elif self.path == "/refill":
            if self.robotArm.connected == False:
                self.send_json_response(
                    {'result': 'ERROR-DISCONNECTED', 'message': 'Robot arm disconnected'})
                return
            helper.ctx.setChocosLeft(helper.ctx.getChocoNum())
            self.send_json_response(
                {'result': 'SUCCESS', 'message': 'Refilled ok'})

        # ----------------------------------------------------------
        #
        #   Unknown command
        #
        # ----------------------------------------------------------
        else:
            self.send_json_response(
                {'result': 'ERROR-UNKNOWN', 'message': 'Unknown command'})

    def do_POST(self):
        return

    def send_json_response(self, json_object):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(
            bytes(json.dumps(json_object, ensure_ascii=False), 'utf-8'))
