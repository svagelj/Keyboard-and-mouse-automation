# -*- coding: utf-8 -*-

defaultWaitTimeSeconds = 1  ## Time between current and next key press
maxNumberOfKeyPresses = 7   ## Maximum number of key presses or mouse movements before stopping the main infinite loop

## This is just an example! Change it how you want.
## This is one cycle that repeats itself over and over
cycle = [
            {"type":"keyboard", "key":"a", "duration":0.1, "wait":0.3},                                 ## this an example of basic key input. "wait" is optional, if there is no "wait" the default is used
            {"type":"keyboard", "key":"shift+d", "duration":0.1, "wait":(0.1, 0.2)},                    ## to use multiple keyboard keys just list all keys with a '+' between each one (no '+' at the beginning and end)
            {"type":"mouse", "key":"left", "duration":0.1, "wait":(0.1, 0.2)},                          ## mouse button support left, middle and right clicks
            {"type":"mouse", "key":(100,100), "duration":0.1, "wait":(2.1, 2.2)},                       ## key for mouse is relative position (x,y) to the current mouse position
            {"type":"mouse", "key":(5000, 5000, "absolute"), "duration":0.1, "wait":(0.1, 0.2)},        ## if key has more than 2 element it is used as absolute position
        ]

## TODO IMPORTANT Remove this line bellow before flight. It is here to prevent you making mistakes before you are ready for them
cycle = []



########################################################################################
#####    Bellow is actual code. You should probably NOT touch it.                  #####
########################################################################################































import random
import time
import ctypes
from ctypes import wintypes


#############################################
## List of all available buttons to click: msdn.microsoft.com/en-us/library/dd375731
keyboardCodeMap = {
    "tab":0x09, 'shift':0x10, "enter":0x0D, "space":0x20, '0':0x30, '1':0x31, '2':0x32, '3':0x33, '4':0x34, '5':0x35, 
    '6':0x36, '7':0x37, '8':0x38, '9':0x39, 'a':0x41, 'b':0x42, 'c':0x43, 'd':0x44, 'e':0x45, 'f':0x46, 'g':0x47, 
    'h':0x48, 'i':0x49, 'j':0x4A, 'k':0x4B, 'l':0x4C, 'm':0x4D, 'n':0x4E, 'o':0x4F, 'p':0x50, 'q':0x51, 'r':0x52, 
    's':0x53, 't':0x54, 'u':0x55, 'v':0x56, 'w':0x57, 'x':0x58, 'y':0x59, 'z':0x5A, "f1":0x70, "f2":0x71, "f3":0x72, 
    "f4":0x73, "f5":0x74, "f6":0x75, "f7":0x76, "f8":0x77, "f9":0x78, "f10":0x79, "f11":0x7A, "f12":0x7B, "left":0x25, 
    "up":0x26, "right":0x27, "down":0x28
    }
mouseCodeMap = {
    "lmClick":0x01, "rmClick":0x02, "mmClick":0x04
    }

## Definitions to use with underlying c library
user32 = ctypes.WinDLL('user32', use_last_error=True)
INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN= 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040

MAPVK_VK_TO_VSC = 0
wintypes.ULONG_PTR = wintypes.WPARAM

## Classes as needed for use with underlying c libraries
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk, MAPVK_VK_TO_VSC, 0)
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))
    
class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))
LPINPUT = ctypes.POINTER(INPUT)

## Functions defining key down, key up
def PressKeyboard(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
    return
def ReleaseKeyboard(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=hexKeyCode, dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
    return

## Functions defining mouse down, mouse up and move
def PressMouse(flags):
    x = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(0, 0, 0, flags, 0, 0))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
    return
def ReleaseMouse(flags):
    x = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(0, 0, 0, flags, 0, 0))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
    return
def MoveMouse(dx,dy, absolute=False):
    flag = MOUSEEVENTF_MOVE
    if absolute == True:
        flag = flag + MOUSEEVENTF_ABSOLUTE

    x = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(dx, dy, 0, flag, 0, 0))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
    return    

######################

## Functions defining the whole key press - i.e. key down, wait, key up
def SendKey(keysArray, delaySeconds=None):

    for key in keysArray:
        PressKeyboard(key)

    if delaySeconds != None:
        time.sleep(delaySeconds)
    
    for key in keysArray:
        ReleaseKeyboard(key)

    return

def SendMouse(mouseButton, delaySeconds=None):

    if mouseButton.lower() == "left":
        mButtonDown = MOUSEEVENTF_LEFTDOWN
        mButtonUP = MOUSEEVENTF_LEFTUP
    elif mouseButton.lower() == "right":
        mButtonDown = MOUSEEVENTF_RIGHTDOWN
        mButtonUP = MOUSEEVENTF_RIGHTUP
    elif mouseButton.lower() == "middle":
        mButtonDown = MOUSEEVENTF_MIDDLEDOWN
        mButtonUP = MOUSEEVENTF_MIDDLEUP
    else:
        print("[ERROR] Invalid chosen mouse button ("+str(mouseButton)+")! Has to be one of these: "+str(["left", "right", "middle"]))

    PressMouse(mButtonDown)

    if delaySeconds != None:
        time.sleep(delaySeconds)

    ReleaseMouse(mButtonUP)

    return

## Main loop
def main():

    i=0
    while True:
        for keyData in cycle:

            ## Duration of key press - time between key down and key up
            duration = None
            if "duration" in keyData.keys():
                duration = keyData["duration"]

            if keyData["type"] == "keyboard":
                ## Press keyboard
                print("keys to press",[keyCode for keyCode in keyData["key"].split("+")])
                keysArray = [ keyboardCodeMap[keyCode] for keyCode in keyData["key"].split("+") ]
                SendKey(keysArray, delaySeconds=duration)
            elif keyData["type"] == "mouse":
                if keyData["key"] in ["left", "right", "middle"]:
                    ## Press mouse
                    SendMouse(keyData["key"], delaySeconds=0.1)
                else:
                    ## Move mouse
                    if len(keyData["key"]) == 2:
                        MoveMouse(keyData["key"][0], keyData["key"][1], absolute=False)
                    else:
                        MoveMouse(keyData["key"][0], keyData["key"][1], absolute=True)
            else:
                print("[ERROR] Unrecognized mouse button type: "+str(keyData)+", must be one of: "+str(["left", "right", "middle"]))

            ## Wait before next move
            if "wait" in keyData.keys():
                if type(keyData["wait"]) in (type(2), type(2.1)):
                    time.sleep(keyData["wait"])
                elif len(keyData["wait"]) == 2:
                    time.sleep(random.uniform(keyData["wait"][0], keyData["wait"][1]))
                else:
                    print("[ERROR] Specified wait time is not as expected. Expected is a number (float or int) or lower and upper bounds for random pick (a, b)")
            else:
                time.sleep(defaultWaitTimeSeconds)

            i=i+1

            if maxNumberOfKeyPresses > 0 and i > maxNumberOfKeyPresses-1:
                return i

        if i == 0:
            return i
        
    return i

if __name__ == "__main__":

    print("program start but waiting 3 seconds before pressing stuff")
    time.sleep(3)
    print("start pressing buttons")

    n = main()

    print("Done pressing "+str(n)+" number of buttons.")

    if n == 0:
        print("The main cycle variable is probably empty. Check if there is another definition of cycle dictionary somewhere else.")
