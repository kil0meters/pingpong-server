import uuid
import sqlite3

from flask import Flask, jsonify, request

from main import app

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

        setArduinoToMachineState()

        return jsonify(machineState)

@app.route('/api/v1/toggle-firing-state', methods=['GET'])
def setFiringState():
    machineState['firingState'] = not machineState['firingState']

    setPin('firingSpeed', 0)
    setPin('oscillationSpeed', 0)
    setPin('topspin', 0)
    setPin('backspin', 0)

    return 'success'

@app.route('/api/v1/get-firing-state', methods=['GET'])
def getFiringState():
    if machineState['firingState'] == True:
        return 'true'
    else:
        return 'false'
