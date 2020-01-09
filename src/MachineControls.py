from flask import Blueprint, current_app, jsonify

machine_controls_api = Blueprint('machine_controls_api', __name__)

@machine_controls_api.route('/api/v1/set-firing-speed/<value>', methods=['GET'])
def setFiringSpeed(value):
    return current_app.config['machineState'].setFiringSpeed(value)

@machine_controls_api.route('/api/v1/set-oscillation-speed/<value>', methods=['GET'])
def setOscillationSpeed(value):
    return current_app.config['machineState'].setOscillationSpeed(value)

@machine_controls_api.route('/api/v1/set-topspin/<value>', methods=['GET'])
def setTopspin(value):
    return current_app.config['machineState'].setTopspin(value)

@machine_controls_api.route('/api/v1/set-backspin/<value>', methods=['GET'])
def setBackspin(value):
    return current_app.config['machineState'].setBackspin(value)

@machine_controls_api.route('/api/v1/toggle-firing-state', methods=['GET'])
def setFiringState():
    return current_app.config['machineState'].toggleFiringState()

@machine_controls_api.route('/api/v1/get-firing-state', methods=['GET'])
def getFiringState():
    if current_app.config['machineState'].machineState['firingState'] == True:
        return 'true'
    else:
        return 'false'


@machine_controls_api.route('/api/v1/get-machine-state', methods=['GET'])
def getMachineState():
    return jsonify(current_app.config['machineState'].machineState)
