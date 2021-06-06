import board
import digitalio
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.rotaryEncoder import encoder
import oledDisplay
from kmk.slider import slider

keyboard = KMKKeyboard()
keyboard.col_pins = (board.GP15, board.GP13, board.GP12)
keyboard.row_pins = (board.GP8, board.GP9, board.GP10, board.GP11)
keyboard.diode_orientation = DiodeOrientation.COLUMNS
keyboard.debug_enabled = True

keyboard.enableEncoder = True
keyboard.encoders = [encoder(board.GP0, board.GP1), encoder(board.GP2, board.GP3)]
keyboard.encoders[0].encMap = [[KC.VOLU, KC.VOLD], [KC.K, KC.J]]
keyboard.encoders[1].encMap = [[KC.RIGHT, KC.LEFT], [KC.X, KC.Z]]

keyboard.enableOled = True
keyboard.oledDisp = oledDisplay.oled(board.GP21, board.GP20, "Hello World")

keyboard.keymap = [
    [KC.Y, None, KC.Z, KC.A, KC.B, KC.C, KC.D, KC.E, KC.F, KC.G, KC.H, KC.TO(1)],
    [KC.Y, None, KC.Z, KC.TO(0), KC.R, KC.S, KC.T, KC.U, KC.V, KC.W, KC.X, KC.TO(0)]
]

# Onboard Pico LED enable
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
led.value = True

keyboard.enableSlider = True
keyboard.sliders = [slider(board.GP26), slider(board.GP27)]


if __name__ == "__main__":
    keyboard.go()
