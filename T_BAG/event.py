from . import utils as u
from . import items as i
# This file contains the event class and the events for the game.

class Event:
    def __init__(self, chance, code:lambda:None):
        self.chance = chance
        self.code = code