print("Starting")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.extensions.rgb import RGB
from kmk.extensions.media_keys import MediaKeys
from kmk.handlers.sequences import send_string, simple_key_sequence

# Set-Up
layers = Layers()
keyboard = KMKKeyboard()
encoder_handler = EncoderHandler()
keyboard.modules = [layers, encoder_handler]

rgb = RGB(pixel_pin=board.D9, 
          num_pixels=4,
          hue_default=165,
          )
keyboard.extensions.append(rgb)
keyboard.extensions.append(MediaKeys())

keyboard.col_pins = (board.D5,board.D6,board.D7,board.D8)
keyboard.row_pins = (board.D4,board.D3,board.D2)
encoder_handler.pins = (
    # Left Encoder
    (board.D1, board.D10, board.D0,),
    # Right Encoder
    (board.SCK, board.MISO, board.MOSI,),
)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

FN = KC.MO(1)
TOG_RGB_LAYER = KC.TG(2)
_______ = KC.TRNS
XXXXXXX = KC.NO

# Macro Functions
def open_file(file_name):
    command = simple_key_sequence([KC.LWIN(KC.S), KC.MACRO_SLEEP_MS(200), send_string(file_name), KC.ENTER])
    return command

def open_instructions():
    # Open a notepad
    open_file("Notepad")
    # Read instructions file
    f = open("instructions.txt", "r")
    # Write the contents of the instructions file into the notepad
    send_string(f.read())
    send_string("Howdy")
    
def open_link(link):
    simple_key_sequence([KC.LWIN(KC.R), KC.MACRO_SLEEP_MS(200), send_string(link), KC.ENTER])

# Macros
# Universal Shortcuts
OPEN_EXCEL = simple_key_sequence([KC.LWIN(KC.LCTRL(KC.LSFT(KC.LALT(KC.X))))])
COPY = simple_key_sequence([KC.LCTRL(KC.C)])
CUT = simple_key_sequence([KC.LCTRL(KC.X)])
PASTE_AS_VALUES = simple_key_sequence([KC.LCTRL(KC.LALT(KC.V)), KC.MACRO_SLEEP_MS(200), KC.V, KC.MACRO_SLEEP_MS(200), KC.ENTER])
UNDO = simple_key_sequence([KC.LCTRL(KC.Z)])
REDO = simple_key_sequence([KC.LCTRL(KC.Y)])

# Programs
# Manually add a key shortcut to any desktop shortcut by right clicking and going to the properties menu.
SOLIDWORKS = open_file('Solidworks')
INSTRUCTIONS = open_instructions()

# Links
RICK_ROLL = open_link('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
GARTHS_WORLD = open_link('https://www.Garths.World')

# Keymaps
keyboard.keymap = [
    # Base Layer
    [
        KC.A, XXXXXXX, OPEN_EXCEL, COPY,
        INSTRUCTIONS, XXXXXXX, XXXXXXX, CUT,
        FN, UNDO, REDO, PASTE_AS_VALUES,
     ],
    # Function Layer
    [
        RICK_ROLL, SOLIDWORKS, XXXXXXX, XXXXXXX,
        GARTHS_WORLD, XXXXXXX, XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
     ],
    # RGB Layer
    [
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        XXXXXXX, KC.RGB_MODE_SWIRL, KC.RGB_MODE_KNIGHT, KC.RGB_MODE_RAINBOW,
        TOG_RGB_LAYER, KC.RGB_MODE_PLAIN, KC.RGB_MODE_BREATHE, KC.RGB_MODE_BREATHE_RAINBOW
     ],
]
encoder_handler.map = [
    (( KC.VOLD, KC.VOLU, KC.MUTE), ( KC.RGB_VAD, KC.RGB_VAI, KC.RGB_TOG)),
    (( KC.VOLD, KC.VOLU, KC.MUTE), ( KC.RGB_HUD, KC.RGB_HUI, TOG_RGB_LAYER)),
    (( KC.VOLD, KC.VOLU, KC.MUTE), ( KC.RGB_HUD, KC.RGB_HUI, TOG_RGB_LAYER)),
]

if __name__ == '__main__':
    keyboard.go()
    