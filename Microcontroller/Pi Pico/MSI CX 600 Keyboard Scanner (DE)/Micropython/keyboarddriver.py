import maindriver as md
import time
import board
import usb_hid
import microcontroller
import sys
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

now = time.monotonic()
keys_pressed = 0

connector_pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17, board.GP18, board.GP19, board.GP20, board.GP21, board.GP22, board.GP26, board.GP27, board.GP28];
keyboard = Keyboard(usb_hid.devices)

keycodes = {'board.GP20|board.GP0': 'R', 'board.GP19|board.GP0': 'P', 'board.GP22|board.GP4': 'LEFT_CONTROL', 'board.GP19|board.GP2': '\xd6', 'board.GP20|board.GP4': 'T', 'board.GP19|board.GP4': '\xdc', 'board.GP19|board.GP7': 'ZERO', 'board.GP20|board.GP5': 'G', 'board.GP19|board.GP5': '\xc4', 'board.GP5|board.GP14': 'SPACE', 'board.GP7|board.GP9': 'ONE', 'board.GP21|board.GP2': 'S', 'board.GP5|board.GP11': 'H', 'board.GP21|board.GP0': 'W', 'board.GP2|board.GP10': 'D', 'board.GP2|board.GP11': 'J', 'board.GP0|board.GP9': 'Q', 'board.GP2|board.GP13': 'K', 'board.GP2|board.GP9': 'A', 'board.GP28_A2|board.GP9': 'Y', 'board.GP4|board.GP9': 'TAB', 'board.GP21|board.GP28_A2': 'X', 'board.GP20|board.GP28_A2': 'V', 'board.GP11|board.GP27_A1': 'SIX', 'board.GP6|board.GP20': 'B', 'board.GP28_A2|board.GP17': 'ENTER', 'board.GP6|board.GP11': 'N', 'board.GP7|board.GP13': 'EIGHT', 'board.GP4|board.GP17': 'BACKSPACE', 'board.GP7|board.GP11': 'SEVEN', 'board.GP7|board.GP10': 'THREE', 'board.GP4|board.GP11': 'Z', 'board.GP18|board.GP0': 'O', 'board.GP28_A2|board.GP10': 'C', 'board.GP20|board.GP27_A1': 'FIVE', 'board.GP18|board.GP2': 'L', 'board.GP28_A2|board.GP11': 'M', 'board.GP4|board.GP26_A0': 'LEFT_SHIFT', 'board.GP0|board.GP10': 'E', 'board.GP0|board.GP11': 'U', 'board.GP18|board.GP7': 'NINE', 'board.GP0|board.GP13': 'I', 'board.GP7|board.GP20': 'FOUR', 'board.GP7|board.GP21': 'TWO', 'board.GP20|board.GP2': 'F'}

def getPinsStrings(pin1, pin2):
    return [str(pin1) + "|" + str(pin2), str(pin2) + "|" + str(pin1)]

def getKeyCodeByPins(pin1, pin2):
    for s in getPinsStrings(pin1, pin2):
        try:
            return keycodes[s]
        except:
            pass
    return ""

def eventCallback(name, pin):
    global keys_pressed
    try:
        pins = pin.split("|")
        ikeycode = getKeyCodeByPins(pins[0], pins[1])
        if(ikeycode == ""):
            print("[WARN] Unidentified Keycodes: " + pin)
            return

        if(hasattr(Keycode, ikeycode) == False):
            print("[WARN] Keycode not valid: " + ikeycode)
            return

        if name == "press":
            keyboard.press(getattr(Keycode, ikeycode))
            return
        elif name == "release":
            keyboard.release(getattr(Keycode, ikeycode))
            return
        else:
            print("[WARN] Unidentified Event from Main-Driver: " + name)
    except:
        print("[ERR] Could not Process Event: " + str(name) + "(" + str(pin) + ")")

def setup():
    md.setup(connector_pins, eventCallback)

def loop():
    global now, keys_pressed
    md.loop()
    took = (time.monotonic() - now)*1000
    print((took,))
    now = time.monotonic()
    return

setup()
while True:
    loop()