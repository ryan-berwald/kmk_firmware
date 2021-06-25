from adafruit_hid.keyboard import Keyboard
from kmk.keys import KC
import rotaryio
import board
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
#from kmk.internal_state import InternalState

consumerKeys = [226, 233, 234, 181, 182, 183]

class encoder:
    def __init__(self, pinA, pinB):
        self.enc = rotaryio.IncrementalEncoder(pinA, pinB)
        self.current_position = None
        self.last_position = 0
        self.encMap = []

def updateEnc(encoder, activeLayer):
    kbd = Keyboard(usb_hid.devices)
    cc = ConsumerControl(usb_hid.devices)

    encoder.current_position = encoder.enc.position
    position_change = encoder.current_position - encoder.last_position
    if encoder.encMap[activeLayer][1].code in consumerKeys or encoder.encMap[activeLayer][0].code in consumerKeys:
        if position_change > 0: #turn right
            cc.send(encoder.encMap[activeLayer][1].code)
        elif position_change < 0: #turn left
            cc.send(encoder.encMap[activeLayer][0].code)
    else:
        if position_change > 0: #turn right
            kbd.send(encoder.encMap[activeLayer][1].code)
        elif position_change < 0: #turn left
            kbd.send(encoder.encMap[activeLayer][0].code)
    encoder.last_position = encoder.enc.position
