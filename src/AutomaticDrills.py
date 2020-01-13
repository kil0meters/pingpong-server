import enum
import json
import uuid
import random
import atexit

import sqlite3

from flask import Blueprint, current_app, request, jsonify

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from MachineState import MachineState
from Errors import InvalidData

automatic_drills_api = Blueprint('automatic_drills_api', __name__)

drillScheduler = BackgroundScheduler()
drillScheduler.start()

atexit.register(lambda: drillScheduler.shutdown())

class NoiseGenerator():
    def __init__(self, minimum, maximum, noiseFactor):
        self.min = minimum
        self.max = maximum

        self.noiseFactor = noiseFactor

class AutomaticDrill():
    def __init__(self, title: str, description: str, firingSpeed: NoiseGenerator,  oscillationSpeed: NoiseGenerator,
                 topspin: NoiseGenerator, backspin: NoiseGenerator, id=None, listIndex=None,):
        self.title = title
        self.description = description

        self.uuid = id
        self.listIndex = listIndex

        self.firingSpeed = firingSpeed
        self.oscillationSpeed = oscillationSpeed
        self.topspin = topspin
        self.backspin = backspin

        self.seed = random.randint(0, 255)

    def fromUUID(drillID: uuid.UUID):
        try: 
            with sqlite3.connect('drills.db') as conn:
                cur = conn.cursor()

                cur.execute('select * from AutomaticDrills where id = ?', (drillID,))
                conn.commit()

                return AutomaticDrill.fromTuple(cur.fetchone())
        except:
            return None

    def fromTuple(tuple):
        return AutomaticDrill(id=tuple[0], listIndex=tuple[1], title=tuple[2], description=tuple[3],
                              firingSpeed=NoiseGenerator(tuple[4], tuple[5], tuple[6]),
                              oscillationSpeed=NoiseGenerator(tuple[7], tuple[8], tuple[9]),
                              topspin=NoiseGenerator(tuple[10], tuple[11], tuple[12]),
                              backspin=NoiseGenerator(tuple[13], tuple[14], tuple[15]))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)

    # database: |id: str|index: int|name: string|description: int|
    #           |firingSpeedMin: int|firingSpeedMax: int|firingSpeedFactor: int|
    #           |oscillationSpeedMin: int|oscillationSpeedMax: int|oscillationSpeedFactor: int|
    #           |firingSpeedMin: int|firingSpeedMax: int|firingSpeedFactor: int|
    #           |firingSpeedMin: int|firingSpeedMax: int|firingSpeedFactor: int|
    def saveToDatabase(self, location: str):
        try: 
            with sqlite3.connect(location) as conn:
                cur = conn.cursor()

                cur.execute('select * from AutomaticDrills')

                drillID = str(uuid.uuid4())
                listIndex = len(cur.fetchall())

                print(listIndex)

                # this is the most godawful line in this codebase
                cur.execute('insert into AutomaticDrills (id, listIndex, name, description,'
                            'firingSpeedMin, firingSpeedMax, firingSpeedFactor,'
                            'oscillationSpeedMin, oscillationSpeedMax, oscillationSpeedFactor,'
                            'topspinMin, topspinMax, topspinFactor,'
                            'backspinMin, backspinMax, backspinFactor)'
                            'values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    (drillID, listIndex, self.title, self.description,
                    self.firingSpeed.min, self.firingSpeed.max, self.firingSpeed.noiseFactor,
                    self.oscillationSpeed.min, self.oscillationSpeed.max, self.oscillationSpeed.noiseFactor,
                    self.topspin.min, self.topspin.max, self.topspin.noiseFactor,
                    self.backspin.min, self.backspin.max, self.backspin.noiseFactor))

                conn.commit()
                return jsonify({'message': 'successfully added automatic drill to database'})
        except:
            raise InvalidData('could not add preset to database')

    def getNewValues(self):
        if self.distributionType == DistributionType.RANDOM:
            self.firingSpeed = random.randint(self.firingSpeed.min, self.firingSpeed.max)
            self.oscillationSpeed = random.randint(self.oscillationSpeed.min, self.oscillationSpeed.max)
            self.topspin = random.randint(self.topspin.min, self.topspin.max)
            self.backspin = random.randint(self.backspin.min, self.backspin.max)

        return MachineState()




@automatic_drills_api.route('/api/v1/add-automatic-drill', methods=['GET'])
def addAutomaticDrill():
    try:
        _title = request.args.get('title', type=str)
        _description = request.args.get('description', type=str)

        _firingSpeedMax = request.args.get('firing-speed-max', type=int)
        _firingSpeedMin = request.args.get('firing-speed-min', type=int)
        _firingSpeedFactor = request.args.get('firing-speed-factor', type=int)

        _oscillationSpeedMax = request.args.get('oscillation-speed-max', type=int)
        _oscillationSpeedMin = request.args.get('oscillation-speed-min', type=int)
        _oscillationSpeedFactor = request.args.get('oscillation-speed-factor', type=int)

        _topspinMax = request.args.get('topspin-max', type=int)
        _topspinMin = request.args.get('topspin-min', type=int)
        _topspinFactor = request.args.get('topspin-factor', type=int)

        _backspinMax = request.args.get('backspin-max', type=int)
        _backspinMin = request.args.get('backspin-min', type=int)
        _backspinFactor = request.args.get('backspin-factor', type=int)

        automaticDrill = AutomaticDrill(title=_title, description=_description,
                                        firingSpeed=NoiseGenerator(_firingSpeedMin, _firingSpeedMax, _firingSpeedFactor),
                                        oscillationSpeed=NoiseGenerator(_oscillationSpeedMin, _oscillationSpeedMax, _oscillationSpeedFactor),
                                        topspin=NoiseGenerator(_topspinMin, _topspinMax, _topspinFactor),
                                        backspin=NoiseGenerator(_backspinMin, _backspinMax, _backspinFactor))

        return automaticDrill.saveToDatabase('drills.db')
    except:
        return InvalidData('did not get all required arguments')

@automatic_drills_api.route('/api/v1/remove-automatic-drill', methods=['GET'])
def removeAutomaticDrill():
    drillID = request.args.get('id')

    try:
        _tmp = uuid.UUID(drillID, version=4)
    except:
        raise InvalidData('Invalid UUID format') 

    with sqlite3.connect('drills.db') as conn:
        cur = conn.cursor()
        cur.execute('delete from AutomaticDrills where id=?', (drillID,))
        conn.commit()
    
    return jsonify({'message': 'successfully removed automatic drill: {}'.format(drillID)})

@automatic_drills_api.route('/api/v1/list-automatic-drills', methods=['GET'])
def listAutomaticDrills():
    with sqlite3.connect('drills.db') as conn:
        cur = conn.cursor()
        cur.execute('select * from AutomaticDrills')
        conn.commit()

        drills = [AutomaticDrill.fromTuple(drill) for drill in cur.fetchall()]

        return json.dumps(drills, default=lambda drill: drill.__dict__)

@automatic_drills_api.route('/api/v1/swap-automatic-drills', methods=['GET'])
def swapAutomaticDrills():
    pass

def printHello():
    print('hello')

@automatic_drills_api.route('/api/v1/start-automatic-drill', methods=['GET'])
def startAutomaticDrill():
    try:
        _tmp = uuid.UUID(request.args.get('uuid'), version=4)
    except:
        InvalidData('not a valid uuid')

    # as a precaution we kill any running drills
    stopAutomaticDrill()

    drill = AutomaticDrill.fromUUID(request.args.get('uuid'))
    drillScheduler.add_job(drill.setNewValues(), 'interval', seconds=3, max_instances=1, id='running_drill', name=drill.uuid)

    return jsonify({'message': 'it worked lol'})

@automatic_drills_api.route('/api/v1/stop-automatic-drill', methods=['GET'])
def stopAutomaticDrill():
    try: 
        drillScheduler.remove_job('running_drill')
        return jsonify({'message': 'it worked lol'})
    except:
        InvalidData('no drill was running')

@automatic_drills_api.route('/api/v1/get-playing-drill', methods=['GET'])
def getPlayingDrill():
    jobs = drillScheduler.get_jobs()

    if jobs != []:
        return jsonify({'uuid': jobs[0].name})
    else:
        return 'null'