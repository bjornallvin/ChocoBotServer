This is a python web server project to control a Dobot Magician robot arm. It is written to be run on a Windows environment.

EXPOSED API:

/connect : Connects to the robot arm. This is normally allready done at startup. But if the python server was allready running when the robot was started. This api can be called.

/pick : Picks the next chocolate. If there are no more left an error message is returned

/home : This will execute the home command to reset the robot arm poistion

/refill : After chocolates have been refilled to the box. Use this api to reset the counter.

/pick/X : Pick specific chocolate slot. X is expected to be a nr from 1 to 11.

/test/X : Pick up at put back slot nr X

/test/all : Test all slots

START SERVER

To start the server just execute "python main.py". There is a bat script for this (launch.bat) but you probably need to edit the paths in that script first

EXTERNAL ACCESS

To expose the web server to the internet use the "serveo.bat" script. This will open up a tunnel from https://chocobot.serveo.net to your local web server.

OR

use "ngrok.exe http 8000" to open the tunnel.
