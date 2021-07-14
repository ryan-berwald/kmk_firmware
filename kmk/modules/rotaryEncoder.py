from kmk.extensions import Extension
from kmk.modules import Module
import rotaryio


class encoder(Module):
    def __init__(self, pins, keyMap):
        self.enc = []
        self.current_position = []
        self.last_position = []
        for x in range(len(pins)):
            self.enc.append(rotaryio.IncrementalEncoder(pins[x][0], pins[x][1]))
            self.current_position.append(self.enc[x].position)
            self.last_position.append(self.enc[x].position)
        self.invert = [True, True]
        self.encMap = keyMap

    def updateEnc(self, keyboard, activeLayer = 0):
        for x in range(len(self.enc)):
            self.current_position[x] = self.enc[x].position
            position_change = self.current_position[x] - self.last_position[x]
            if self.invert[x]:
                if position_change < 0: #turn right
                    keyboard.tap_key(self.encMap[x][keyboard.active_layers[len(keyboard.active_layers)-1]][0])
                elif position_change > 0: #turn left
                    keyboard.tap_key(self.encMap[x][keyboard.active_layers[len(keyboard.active_layers)-1]][1])
            else:
                if position_change > 0: #turn right
                    keyboard.tap_key(self.encMap[x][keyboard.active_layers[len(keyboard.active_layers)-1]][0])
                elif position_change < 0: #turn left
                    keyboard.tap_key(self.encMap[x][keyboard.active_layers[len(keyboard.active_layers)-1]][1])
            if keyboard.debug_enabled:
                if self.current_position != self.last_position:
                    print(repr(self))
            self.last_position[x] = self.current_position[x]

    def on_runtime_enable(self, keyboard):
        self.debug_enabled = keyboard.debug_enabled
        return

    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        self.updateEnc(keyboard)

        return keyboard

    def after_matrix_scan(self, keyboard):
        '''
        Return value will be replace matrix update if supplied
        '''
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def __repr__(self):
        return 'ENCODER({})'.format(self._to_dict())

    def _to_dict(self):
        return {
            'Encoder': self.enc,
            'Current Position': self.current_position,
            'Last Position': self.last_position,
            'Invert': self.invert,
            'Encoder Map': self.encMap
        }