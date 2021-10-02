import ctypes
import difflib
import operator
import sys
import time

import pyautogui
# from pynput import keyboard
import pydirectinput
import pytesseract
import win32gui
from PIL import Image, ImageGrab
from pyautogui import press

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pyautogui.FAILSAFE = False

w = win32gui

enemies = ['Guerreiro de Magma']


# CHECK BEFORE STARTING:
# Banker position on screen

def find_target():
    img = ImageGrab.grab((481, 47, 633, 62))
    img = img.convert('L')
    img.save("temp.png")
    name = pytesseract.image_to_string(
        Image.open('temp.png'), config='--psm 7')
    try:
        print(name)
      
        if(len(name.strip().replace(" ", ""))  < 6):
            raise Exception("Erro na leitura")

        return name.strip()
    except ValueError:
        print("ERROR: TARGET NOT CORRECTLY DETECTED")
        return ""
    except Exception:
        return ""


def valid_target():
    try:
        name = find_target()
    except NameError:
        return False

    for enemy in enemies:
        diff = difflib.SequenceMatcher(None, name.replace(
            "|", "").replace(")", "").strip(), enemy).ratio()

        print(diff)

        if(diff >= 0.7):
            return True

    return False


def check_pause():
    global pause
    global pauseCounter
    if pyautogui.position() == (0, 0):
        pauseCounter += 1
    else:
        pause = False
        pauseCounter = 0

    if pauseCounter > 0:
        pause = True


pause = False
pauseCounter = 0

while True:
    program = w.GetWindowText(w.GetForegroundWindow()).strip()
    check_pause() 
    if program == 'The Classic PW' and not pause:
        print("Attempting to find target")

        press('f1')
        time.sleep(.5)
        press('f1')
        time.sleep(.5)
        press('f1')
        time.sleep(.5)
        press('f1')

        if not valid_target():
            press('tab')
        start = time.time()
        if valid_target():
            while valid_target():
                print("LOCKED ON!")
                press('f4')
                time.sleep(.5)
                end = time.time()
                if end - start > 15 and not valid_target():
                    time.sleep(.5)
                    break

    else:
        print("PWI not on screen or script paused")
        time.sleep(10)
