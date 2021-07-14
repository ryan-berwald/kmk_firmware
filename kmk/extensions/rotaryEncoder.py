from kmk.extensions import Extension
from kmk.keys import KC
from kmk.extensions.media_keys import MediaKeys
from kmk.keycodes import KC
from kmk.extensions import Extension
import rotaryio

#from kmk.internal_state import InternalState


class encoder(Extension):
    def __init__(self, pinA, pinB):
        self.enc = rotaryio.IncrementalEncoder(pinA, pinB)
        self.current_position = None
        self.last_position = 0
        self.encMap = []

    def updateEnc(encoder, activeLayer, keyboard):
        encoder.current_position = encoder.enc.position
        position_change = encoder.current_position - encoder.last_position
        if encoder.encMap[activeLayer][1].code in KC.MediaKeys.keys or encoder.encMap[activeLayer][0].code in consumerKeys:
            if position_change > 0: #turn right
                keyboard.tap_key(encoder.encMap[activeLayer][1].code)
            elif position_change < 0: #turn left
                cc.send(encoder.encMap[activeLayer][0].code)
        else:
            if position_change > 0: #turn right
                kbd.send(encoder.encMap[activeLayer][1].code)
            elif position_change < 0: #turn left
                kbd.send(encoder.encMap[activeLayer][0].code)
        encoder.last_position = encoder.enc.position
