#!bin/python3

from flask import Flask, jsonify, request
#import RPi.GPIO as IO
import serial
import sqlite3
import uuid
import time
import os

import AutomaticDrills
import RemotePresets

debug = False
try:
    _tmp = os.environ['DEBUG']
    debug = True
except:
    pass

if debug != True:
    ser = serial.Serial('/dev/ttyACM0', 9600)

app = Flask(__name__)

machineState = {
            'firingSpeed': 0,
            'oscillationSpeed': 0,
            'topspin': 0,
            'backspin': 0,
            'firingState': False,
        }

def arduino_write(byte_array):
    if debug != True:
        ser.write(byte_array)

class InvalidData(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidData)
def handle_invalid_data(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def setPin(pinName, value):
    value = int(value)
    if value in range(0, 256):
        machineState[pinName] = value
        if pinName == 'firingSpeed':
            arduino_write(bytes([1, value])) # ord('R') = 82
        if pinName == 'oscillationSpeed':
            arduino_write(bytes([2, value])) # ord('O') = 79
        if pinName == 'topspin':
            arduino_write(bytes([3, value]))
        if pinName == 'backspin':
            arduino_write(bytes([4, value]))
        return jsonify(machineState)
    else:
        raise(InvalidData('value not in range(0, 256)'))

def setArduinoToMachineState():
    setPin('firingSpeed', machineState['firingSpeed'])
    setPin('oscillationSpeed', machineState['oscillationSpeed'])
    setPin('topspin', machineState['topspin'])
    setPin('backspin', machineState['backspin'])

@app.route('/api/v1/set-firing-speed/<value>', methods=['GET'])
def setFiringSpeed(value):
    return setPin('firingSpeed', value)

@app.route('/api/v1/set-oscillation-speed/<value>', methods=['GET'])
def setOscillationSpeed(value):
    return setPin('oscillationSpeed', value)

@app.route('/api/v1/set-topspin/<value>', methods=['GET'])
def setTopspin(value):
    return setPin('topspin', value)

@app.route('/api/v1/set-backspin/<value>', methods=['GET'])
def setBackspin(value):
    return setPin('backspin', value)

@app.route('/api/v1/get-machine-state', methods=['GET'])
def getMachineState():
    return jsonify(machineState)

if __name__ == '__main__':
    db = sqlite3.connect('drills.db')
    db.execute('create table if not exists RemotePresets'
            '(id STRING PRIMARY KEY, name STRING, firingSpeed INTEGER, oscillationSpeed INTEGER, topspin INTEGER, backspin INTEGER)')

    db.execute('create table if not exists AutomaticDrills'
                '(id STRING PRIMARY KEY, name STRING, description STRING,'
                'firingSpeedMin INTEGER, firingSpeedMax INTEGER,'
                'oscillationSpeedMin INTEGER, oscillationSpeedMax INTEGER,'
                'topspinMin INTEGER, topspinMax INTEGER)')

    db.close()


    if debug == True:
        app.run(host='127.0.0.1', port=5858)
    else:
        app.run(host='0.0.0.0', port=5858)
