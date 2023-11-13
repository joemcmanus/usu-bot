#!/usr/bin/env python3
# File    : server.py  - a web interface to display coding vulnerabilities
# Author  : Joe McManus josephmc@alumni.cmu.edu
# Version : 0.2  11/07/2023 Joe McManus
# Copyright (C) 2023 Joe McManus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, Markup, request, make_response, escape, render_template
from adafruit_motorkit import MotorKit
import time
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

kit = MotorKit()

app = Flask(__name__)
auth = HTTPBasicAuth()

users = { "aggies": generate_password_hash("hackthebot")}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route("/")
def index():
    titleText = "Python Robot Examples"
    bodyText = Markup(
        """
    <a href=/drive/1> Forward </a><br>
    <a href=/drive/2> Back </a><br>
    <a href=/drive/3> Left </a><br>
    <a href=/drive/4> Right </a><br>
    """
    )
    return render_template("templatecss.html", bodyText=bodyText, titleText=titleText)


@app.route("/drive/<urlDir>/")
@auth.login_required
def drive(urlDir):
    titleText = "Drive the bot"
    if urlDir == "1":
        kit.motor1.throttle = 1.0
        kit.motor2.throttle = 1.0
        time.sleep(1)
        direction = "Forward"
        link = "/drive/1"
    if urlDir == "2":
        kit.motor1.throttle = -1.0
        kit.motor2.throttle = -1.0
        time.sleep(1)
        direction = "Backward"
        link = "/drive/2"
    if urlDir == "3":
        kit.motor1.throttle = 1.0
        kit.motor2.throttle = 0.5
        time.sleep(1)
        direction = "Left"
        link = "/drive/3"
    if urlDir == "4":
        kit.motor1.throttle = 0.5
        kit.motor2.throttle = 1.0
        time.sleep(1)
        direction = "Right"
        link = "/drive/4"
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    bodyText = Markup(
        "Moving " + direction + "<br> <a href=" + link + ">" + direction + "</a><br>"
    )
    return render_template("templatecss.html", bodyText=bodyText, titleText=titleText)

@app.route('/about')
def about():
    titleText="About"
    bodyText=Markup('''A simple flask app to show using Flask and ROS <br>
    <br> Source code can be found at : <a href=https://github.com/joemcmanus/tankbotROS> github </a> <br>
    <br><br>
    Thanks - Joe 
    ''')
    return render_template('templatecss.html', bodyText=bodyText, titleText=titleText)



if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=80)
