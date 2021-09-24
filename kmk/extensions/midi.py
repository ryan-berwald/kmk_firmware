# Write your code here :-)
import board
from analogio import AnalogIn
import usb_midi
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from math import ceil
from kmk.extensions import Extension

class Potentiometer(Extension):
    def __init__(self, analogPins, maxPotVal = 65220, change = 2):
        self.pots = []
        for pin in analogPins:
            self.pots.append(AnalogIn(pin))
        self._maxPotVal = maxPotVal # Max value of pots
        self.change = 2 # How much of a change in percentage to react to
        self.midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
        self.prevVal = [0, 0]
        self.vols = [0, 0]
        for pot in self.pots:
            self.getPotVals()

    def checkVal(self):
        self.getPotVals()
        try:
            for idx, vol in enumerate(self.vols):
                if abs(vol - self.prevVal[idx]) > self.change:
                    self.midi.send([ControlChange(idx, ceil(vol), channel=idx)])
                    self.prevVal[idx] = vol
        except Exception as e:
            print(e)

    def getPotVals(self):
        try:
            for idx, pot in enumerate(self.pots):
                self.vols[idx] = ceil((pot.value/self._maxPotVal) *100)
        except Exception as e:
            print("Midi" + e)

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        return

    def before_matrix_scan(self, sandbox):
        self.checkVal()


    def after_matrix_scan(self, sandbox):
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return
