#!bin/python3

from flask import Flask, jsonify, request
#import RPi.GPIO as IO
import serial
import sqlite3
import uuid
import time
import os

if os.environ['DEBUG'] != 'true':
    ser = serial.Serial('/dev/ttyACM0', 9600)

db = sqlite3.connect('drills.db')
db.execute('create table if not exists RemotePresets'
           '(id STRING PRIMARY KEY, name STRING, firingSpeed INTEGER, oscillationSpeed INTEGER, topspin INTEGER, backspin INTEGER)')
db.close()

app = Flask(__name__)

machineState = {
            'firingSpeed': 0,
            'oscillationSpeed': 0,
            'topspin': 0,
            'backspin': 0,
            'firingState': False,
        }

def arduino_write(byte_array):
    if os.environ['DEBUG'] != 'true':
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

@app.route('/api/v1/add-preset', methods=['GET'])
def savePreset():
    try:
        preset_uuid = str(uuid.uuid4())

        _name = request.args.get('name', default="unnammed", type=str)
        _firingSpeed = request.args.get('firingSpeed', default=0, type=int)
        _oscillationSpeed = request.args.get('oscillationSpeed', default=0, type=int)
        _topspin = request.args.get('topspin', default=0, type=int)
        _backspin = request.args.get('backspin', default=0, type=int)

        preset = (preset_uuid, _name, _firingSpeed, _oscillationSpeed, _topspin, _backspin)
    except:
        raise InvalidData('did not find all required arguments: name, firingSpeed, oscillationSpeed, topspin, backspin')

    try: 
        with sqlite3.connect('drills.db') as conn:
            print('Adding {} to database'.format(preset))
            cur = conn.cursor()
            cur.execute('insert into RemotePresets (id, name, firingSpeed, oscillationSpeed, topspin, backspin)'
                'values(?,?,?,?,?,?)', preset)
            conn.commit()
            return jsonify({'message': 'successfully added preset to database'})
    except:
        conn.rollback()
        conn.close()
        raise InvalidData('could not add preset to database')

@app.route('/api/v1/remove-preset/<presetUUID>', methods=['GET'])
def removePreset(presetUUID):
    try:
        val = uuid.UUID(presetUUID, version=4)
    except:
        raise InvalidData('Invalid UUID format') 

    with sqlite3.connect('drills.db') as conn:
        cur = conn.cursor()
        cur.execute('delete from RemotePresets where id=?', (presetUUID,))
        conn.commit()
    
    return jsonify({'message': 'successfully removed preset: {}'.format(presetUUID)})

@app.route('/api/v1/list-remote-presets', methods=['GET'])
def listRemotePresets():
    with sqlite3.connect('drills.db') as conn:
        cur = conn.cursor()
        cur.execute('select * from RemotePresets')
        conn.commit()
        return jsonify(cur.fetchall())

@app.route('/api/v1/set-machine-state-to-preset/<presetUUID>')
def setMachineStateToPreset(presetUUID):
    try:
        _tmp = uuid.UUID(presetUUID, version = 4)
    except:
        raise InvalidData('Invalid UUID')

    with sqlite3.connect('drills.db') as conn:
        cur = conn.cursor()
        cur.execute('select * from RemotePresets where id=?', (presetUUID,))
        conn.commit()

        result = cur.fetchone()

        if result == None:
            conn.rollback()
            conn.close()
            raise InvalidData('could not find preset with specified UUID')

        # format: id, name, firingSpeed, oscillationSpeed, topspin, backspin
        machineState['firingSpeed'] = result[2]
        machineState['oscillationSpeed'] = result[3]
        machineState['topspin'] = result[4]
        machineState['backspin'] = result[5]

        return jsonify(machineState)

@app.route('/api/v1/toggle-firing-state', methods=['GET'])
def setFiringState():
    machineState['firingState'] = not machineState['firingState']
    return 'success'

@app.route('/api/v1/get-firing-state', methods=['GET'])
def getFiringState():
    if machineState['firingState'] == True:
        return 'true'
    else:
        return 'false'

if __name__ == '__main__':
    if os.environ['DEBUG'] == 'true':
        app.run(host='127.0.0.1', port=8080)
    else:
        app.run(host='0.0.0.0', port=8080)
