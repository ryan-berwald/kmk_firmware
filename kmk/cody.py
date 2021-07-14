import board
import digitalio
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.rotaryEncoder import encoder

keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys())
keyboard.col_pins = (board.GP15, board.GP13, board.GP12)
keyboard.row_pins = (board.GP8, board.GP9, board.GP10, board.GP11)
keyboard.diode_orientation = DiodeOrientation.COLUMNS
keyboard.debug_enabled = True

pins = [[board.GP0, board.GP1], [board.GP2, board.GP3]]
encMap = [[[KC.VOLU, KC.VOLD], [KC.K, KC.J]],[[KC.MEDIA_NEXT_TRACK,KC.MEDIA_PREV_TRACK], [KC.X, KC.Z]]]
keyboard.modules.append(encoder(pins, encMap))

keyboard.keymap = [
    [KC.AUDIO_MUTE, None, KC.MEDIA_PLAY_PAUSE, KC.F13, KC.F14, KC.C, KC.D, KC.E, KC.F, KC.G, KC.H, KC.I],
    [KC.Y, None, KC.Z, KC.L, KC.R, KC.S, KC.T, KC.U, KC.V, KC.W, KC.X, KC.J]
]

# Onboard Pico LED enable
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
led.value = True


if __name__ == "__main__":
    keyboard.go()