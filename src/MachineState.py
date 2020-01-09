from flask import jsonify

def arduino_write(debug, byte_array):
    if debug != True:
        ser.write(byte_array)

class MachineState():
    def __init__(self, debug=False):
        self.machineState = machineState = {
            'firingSpeed': 0,
            'oscillationSpeed': 0,
            'topspin': 0,
            'backspin': 0,
            'firingState': False,
        }
        self.debug = debug
    
    def setPin(self, pinName, value, writeToState=True):
        value = int(value)
        if value in range(0, 256):
            if writeToState == True:
                self.machineState[pinName] = value
            if self.machineState['firingState'] == True:
                print('Setting PIN {} to {}'.format(pinName, value))
                if pinName == 'firingSpeed':
                    arduino_write(self.debug, bytes([1, value])) # ord('R') = 82
                if pinName == 'oscillationSpeed':
                    arduino_write(self.debug, bytes([2, value])) # ord('O') = 79
                if pinName == 'topspin':
                    arduino_write(self.debug, bytes([3, value]))
                if pinName == 'backspin':
                    arduino_write(self.debug, bytes([4, value]))
            return jsonify(self.machineState)
        else:
            raise(InvalidData('value not in range(0, 256)'))

    def setFiringSpeed(self, value, writeToState=True):
        return self.setPin('firingSpeed', value, writeToState) 

    def setOscillationSpeed(self, value, writeToState=True):
        return self.setPin('oscillationSpeed', value, writeToState) 

    def setTopspin(self, value, writeToState=True):
        return self.setPin('topspin', value, writeToState) 

    def setBackspin(self, value, writeToState=True):
        return self.setPin('backspin', value, writeToState) 
    
    def toggleFiringState(self):
        self.machineState['firingState'] = not self.machineState['firingState']

        if self.machineState['firingState'] == True:
            self.setPin('firingSpeed', self.machineState['firingSpeed'], writeToState=False)
            self.setPin('oscillationSpeed', self.machineState['oscillationSpeed'], writeToState=False)
            self.setPin('topspin', self.machineState['topspin'], writeToState=False)
            self.setPin('backspin', self.machineState['backspin'], writeToState=False)
        else:
            self.setPin('firingSpeed', 0, writeToState=False)
            self.setPin('oscillationSpeed', 0, writeToState=False)
            self.setPin('topspin', 0, writeToState=False)
            self.setPin('backspin', 0, writeToState=False)
        return jsonify(self.machineState)

machineState = MachineState()