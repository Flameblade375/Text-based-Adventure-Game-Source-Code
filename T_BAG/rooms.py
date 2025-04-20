from . import utils as u
from . import event as e
from . import items as i
from . import beings as b
# This file contains the room class and the rooms for the game.

class Exit:
    def __init__(self, exit_type, needs=None):
        self.type = exit_type
        self.needs = needs or []

class Room:
    def __init__(
            self,
            directions=None,
            items:list[i.Item]=None,
            monster=None,
            info='',
            exit:Exit=None,
            events:list[e.Event]=[],
            rtype:str='house',
        ):
        self.directions = directions or {}
        self.items = items or []
        self.monster = monster
        self.info = info
        self.exit = exit
        self.events = events
        self.type = rtype

roomDirectionText = {
    'house': {
        'north': 'There is a door to the north',
        'south': 'There is a door to the south',
        'east': 'There is a door to the east',
        'west': 'There is a door to the west',
        'up': 'There is a staircase going up',
        'down': 'There is a staircase going down',
    },
}

def directions(currentRoom):
    text = ''
    if currentRoom in rooms:
        for direction in rooms[currentRoom].directions:
            if direction in roomDirectionText[rooms[currentRoom].type]:
                text += roomDirectionText[rooms[currentRoom].type][direction] + '\n'
    return text

# A dictionary linking a room to other rooms
rooms = {
    'Hall': Room(
        directions = {
            'south': 'Kitchen',
            'east': 'Dining Room',
        },
        items = [
            i.Item('key'),
        ],
        info = 'You are in a dark, dusty hall.',
    ),
    'Kitchen': Room(
        directions = {
            'north': 'Hall',
            'east': 'Garden',
        },
        monster = b.Monster(
            m_type = 'bear',
            health = 7,
            attack = 4,
            defence = 2,
            needs = [
                'potion',
            ],
            kill_text = 'The bear eats you.',
            killed_text = 'You killed the bear with a potion!',
        ),
        info = 'You are in a large kitchen.',
    ),
    'Dining Room': Room(
        directions = {
            'west': 'Hall',
            'south': 'Garden',
        },
        items = [
            i.Item('potion'),
        ],
        info = 'You are in a large dining room.',
    ),
    'Garden': Room(
        directions = {
            'north': 'Dining Room',
            'west': 'Kitchen',
        },
        info = 'You are in a beautiful garden, with a locked gate leading \
out of the garden.',
        exit = Exit(
            exit_type = 'gate',
            needs = [
                'key'
            ],
        ),
    )
}