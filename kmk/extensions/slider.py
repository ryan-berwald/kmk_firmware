from analogio import AnalogIn
import board
import usb_hid
#GP27 GP276

class slider:
    def __init__(self, pin):
        self.slider = AnalogIn(pin)
        self.value = self.slider.value

    def getValue(self):
        self.value = self.slider.value
        return self.value



