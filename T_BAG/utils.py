import time
import sys
import os
import random
# This file contains the utility functions for the game.
# It contains the functions for the game loop, the commands, and the player class.

global DEVMODE, DEVPIN
DEVMODE = False
DEVPIN = 'alexander793510'

def DEBUG(*args):
    if DEVMODE:
        print('DEBUG:', *args)


def rickroll(times=1):
    print("you hear a strange noise...")
    time.sleep(1)
    for _ in range(times):
        print("Never gonna give you up,")
        time.sleep(1)
        print("Never gonna let you down,")
        time.sleep(1)
        print("Never gonna run around and desert you.")
        time.sleep(1)
        print("Never gonna make you cry,")
        time.sleep(1)
        print("Never gonna say goodbye,")
        time.sleep(1)
        print("Never gonna tell a lie and hurt you.")
        time.sleep(1)
    return


def handle_devmode():
    devmode = input('Do you want to run in devmode? yes/no: ').strip().lower().startswith('y')
    if devmode:
        pin = input("Enter the pin to enter devmode: ").strip()
        if pin == DEVPIN:
            print("Entering devmode...")
            DEVMODE = True
        else:
            print("Incorrect pin.")
            DEVMODE = False
    else:
        DEVMODE = False