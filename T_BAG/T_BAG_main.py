import random
import time
import sys
from . import utils as u
from . import beings as b
from . import items as i
from . import event as e
from . import rooms as r
from . import commands as c
# This is the main file for the game. It contains the main game loop and the
# main game logic. It also contains the room and item classes, as well as the
# commands and the player class.


def show_instructions():
    # Print a main menu and the commands
    print(
        """
        RPG Game
        ========

        Get to the Garden with the key
        Avoid the monsters!
        """
    )
    c.show_commands()


def show_status():
    # Print the player's current status
    print('---------------------------')
    print('Health: ' + str(player.health))
    print('Attack: ' + str(player.attack_power))
    print('Defence: ' + str(player.defence))
    print('XP: ' + str(player.XP))
    print('Level: ' + str(player.level))
    # Print the current inventory
    print('Inventory: ' + str(player.inventory))
    print(r.rooms[player.current_room].info)
    print("---------------------------")


# A player, which initially has an empty inventory
player = b.Player(
    current_room = 'Hall',
    last_room = 'Hall',
    health = 10,
    attack = 3,
    defence = 1,
    name = 'Player',
    inventory = i.Inventory(),
    XP=0,
    LVL=1,
)

def move(*directions):
    global player
    for direction in directions:
        if (r.rooms[player.current_room].directions and
            direction in r.rooms[player.current_room].directions):
            player.last_room = player.current_room
            player.current_room = r.rooms[player.current_room].directions[direction]
        elif u.DEVMODE and direction in r.rooms:
            player.last_room = player.current_room
            player.current_room = direction
        else:
            print(f'You can\'t go {direction}!')

def get(*item_names):
    global player
    # If the room contains an item, and the item is the one they want to get
    for item_name in item_names:
        # Find the item in the room by its name
        item = next((i for i in r.rooms[player.current_room].items if i.name == item_name), None)
        if item:
            # Add the item to their inventory
            if player.inventory.add(item):
                # Remove the item from the room
                r.rooms[player.current_room].items.remove(item)
            else:
                continue
        else:
            # Tell them they can't get it
            print(f'Can\'t get {item_name}!')

def quit(time_to_wait: int=0):
    try:
        if type(time_to_wait) == list:
            time_to_wait = time_to_wait[0]
        if type(time_to_wait) == str:
            time_to_wait = int(time_to_wait)
    except ValueError:
        print('Invalid time to wait!')
        sys.exit()
    print('Quitting...')
    time.sleep(time_to_wait)
    sys.exit()

def drop(*item_names):
    global player
    # If the players inventory contains an item, the player can drom that item
    for item_name in item_names:
        # Find the item in the inventory by its name
        item = next((i for i in player.inventory.items if i.name == item_name), None)
        if item:
            # Add the item to the room
            r.rooms[player.current_room].i.append(item)
            # Remove the item from their inventory
            u.DEBUG(player.inventory.remove(item))
            print(f'Dropped {item_name}!')
        else:
            # Tell them they can't drop it
            print(f'Can\'t drop {item_name}!')

def battle(player:b.Player, monster:b.Monster):
    print(f'A {monster.type} attacks you!')
    print(f'Enemy health: {monster.health}')
    print(f'Your health: {player.health}')
    while player.health > 0 and monster.health > 0:
        input_ = input('Do you want to run or attack? ').strip().lower()
        if input_ == 'run':
            player.current_room = player.last_room
            print('You ran away!')
            return
        elif input_ == 'attack':
            
            player.attack(monster)
            if monster.health > 0:
                monster.attack(player)
                print(f'Enemy health: {monster.health}')
                print(f'Your health: {player.health}')
            else:
                print(f'You killed the {monster.type}!')
                print(f'Your health: {player.health}')
                return
        else:
            print('Invalid command!')
    if player.health <= 0:
        player.die()
        return

def handle_monster(room: r.Room):
    global player
    monster = room.monster
    if type(monster) == b.Monster:
        if monster.health > 0:
            if (monster.needs and
                all(player.inventory.has(x)
                for x in monster.needs)):
                if monster.killed_text:
                    print(monster.killed_text)
                elif monster.type:
                    print(
                        'You killed the ' +
                        monster.type +
                        '!'
                    )
                else:
                    print('You killed the monster!')
                room.monster = None
            else:
                battle(player, monster)

commands = {
    'go': {
        "command": move,
        "description": "Move to a different room",
        "args": "one or more diractions",
    },
    'get': {
        "command": get,
        "description": "Get item items from the room",
        "args": "one or more items",
    },
    'quit': {
        "command": quit,
        "description": "Quit the game",
        "args": "seconds to wait before quitting",
    },
    'help': {
        "command": c.show_commands,
        "description": "Show the commands",
        "args": "number of commands to show. 0 to show all",
    },
    'drop': {
        "command": drop,
        "description": "Drop an item into the current room",
        "args": "one or more items",
    }
}


def main():
    # Show the instructions
    print("Loading...")
    time.sleep(0.1)
    print("Setting up player...")
    time.sleep(0.1)
    print("Setting up command functions...")
    time.sleep(0.1)
    print("Setting up commands dictionary...")
    time.sleep(0.1)
    print("Finishing up...")
    time.sleep(0.1)
    print("Done!\n\n")
    show_instructions()

    # Loop forever
    while True:

        show_status()

        # Get the player's next 'move'
        # parse_command() breaks it up into a list array
        # eg typing 'go east' would give the list:
        # ['go', 'east'] because go is a commannd and east is the direction,
        # but if a multiword command is added to the game, it will show
        # something like this (the bit where it says 'multiword command'
        # is where the multiword command would be, and the bit where it says
        # 'argument(s)' is where the argument(s) would be):
        # ['multiword command', 'argument(s)']
        command = ''
        while command == '':
            command = input('>')

        command = c.parse_command(command)

        room = r.rooms[player.current_room]
        if type(room) == r.Room:
            if (room.exit and
                room.exit.needs):
                if all(player.inventory.has(x) 
                    for x in room.exit.needs):
                    print('You escaped the house... YOU WIN!')
                    sys.exit()
                else:
                    print(
                        'You need ' +
                        ', '.join(r.rooms[player.current_room].exit.needs) +
                        ' to escape!'
                    )

            if command and len(command) >= 2:
                commands[command[0]]["command"](*command[1:])
            else:
                print('Invalid command!')

            room = r.rooms[player.current_room]

            if room.monster:
                handle_monster(room)

if __name__ == '__main__':
    u.handle_devmode()
    main()
