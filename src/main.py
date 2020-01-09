#!bin/python3

from flask import Flask, jsonify, request, current_app
import flask
#import RPi.GPIO as IO
import serial
import sqlite3
import uuid
import time
import os

import AutomaticDrills
from MachineState import MachineState
from RemotePresets import remote_presets_api
from MachineControls import machine_controls_api
from Errors import InvalidData, error_blueprint

if __name__ == '__main__':
    debug = False
    try:
        _tmp = os.environ['DEBUG']
        debug = True
    except:
        pass

    if debug != True:
        ser = serial.Serial('/dev/ttyACM0', 9600)

    db = sqlite3.connect('drills.db')
    db.execute('create table if not exists RemotePresets'
            '(id STRING PRIMARY KEY, name STRING, firingSpeed INTEGER, oscillationSpeed INTEGER, topspin INTEGER, backspin INTEGER)')

    db.execute('create table if not exists AutomaticDrills'
                '(id STRING PRIMARY KEY, name STRING, description STRING,'
                'firingSpeedMin INTEGER, firingSpeedMax INTEGER,'
                'oscillationSpeedMin INTEGER, oscillationSpeedMax INTEGER,'
                'topspinMin INTEGER, topspinMax INTEGER)')

    db.close()

    app = Flask(__name__)
    app.register_blueprint(remote_presets_api)
    app.register_blueprint(machine_controls_api)
    app.register_blueprint(error_blueprint)

    app.config['machineState'] = MachineState(debug=debug)

    if debug == True:
        app.run(host='127.0.0.1', port=5858)
    else:
        app.run(host='0.0.0.0', port=5858)
