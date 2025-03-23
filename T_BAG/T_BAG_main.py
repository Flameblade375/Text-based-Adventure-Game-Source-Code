import random
import time
import sys


# Classes:
class Exit:
    def __init__(self, exit_type, needs=None):
        self.type = exit_type
        self.needs = needs or []

class Room:
    def __init__(self, directions=None, items=None, monster=None, info='', exit:Exit=None):
        self.directions = directions or {}
        self.items = items or []
        self.monster = monster
        self.info = info
        self.exit = exit

class Being:
    def __init__(self, health, attack, defence, name):
        self.health = health
        self.attack_power = attack
        self.defence = defence
        self.name = name

    def calculate_damage(self, target):
        if issubclass(type(target), Being):
            max_damage = self.attack_power + 2
            min_damage = max_damage // 2
            base_damage = random.randint(min_damage, max_damage)
            damage = base_damage - target.defence
            if damage < 0:
                damage = 0
            return damage

    def attack(self, target):
        if issubclass(type(target), Being):
            end_damage = self.calculate_damage(target)
            target.health -= end_damage
            print(
                str(self.name) +
                ' attacked ' +
                str(target.name) +
                ' for ' +
                str(end_damage) +
                ' damage! ' +
                str(target.name) +
                ' had ' +
                str(target.defence) +
                ' defence! '
            )
            if target.health <= 0:
                target.health = 0
                target.die()

    def die(self):
        print(f'{self.name} died!')
        if type(self) == Player:
            print('Game Over!')
            sys.exit()

class Monster(Being):
    def __init__(self, m_type, health, attack, defence, needs=None, kill_text='', killed_text=''):
        super().__init__(health, attack, defence, m_type)
        self.type = m_type
        self.needs = needs or []
        self.kill_text = kill_text
        self.killed_text = killed_text

class Inventory:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)
        print(f'{item} got!')

    def has(self, item):
        return item in self.items

    def __str__(self):
        return ', '.join(self.items) if self.items else 'empty'

class Player(Being):
    def __init__(
            self,
            current_room,
            last_room,
            health,
            attack,
            defence,
            name,
            inventory:Inventory = Inventory(),
            XP=0,
            LVL=1
        ):
        super().__init__(health, attack, defence, name)
        self.current_room = current_room
        self.last_room = last_room
        self.inventory = inventory
        self.XP = XP
        self.level = LVL


def DEBUG(*args):
    print('DEBUG:', *args)


def show_commands(commands_to_show=0):
    try:
        if type(commands_to_show) == list:
            commands_to_show = commands_to_show[0]
        if type(commands_to_show) == str:
            commands_to_show = int(commands_to_show)
    except ValueError:
        print('invalid number of commands to show!')
        commands_to_show = 0
    # Print a list of the commands
    print(
        """
        Commands:
        """
    )
    if commands_to_show == 0:
        commands_to_show = len(commands)
    shown_commands = 0
    for key, value in commands.items():
        print(f'        {key} - {value["description"]} - {value["args"]}')
        shown_commands += 1
        if shown_commands >= commands_to_show:
            return


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
    show_commands()


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
    print(rooms[player.current_room].info)
    print("---------------------------")


# A player, which initially has an empty inventory
player = Player(
    current_room = 'Hall',
    last_room = 'Hall',
    health = 10,
    attack = 3,
    defence = 1,
    name = 'Player',
    inventory = Inventory(),
    XP=0,
    LVL=1,
)
                                                                              
# A dictionary linking a room to other rooms
rooms = {
    'Hall': Room(
        directions = {
            'south': 'Kitchen',
            'east': 'Dining Room',
        },
        items = [
            'key',
        ],
        info = 'You are in a dark, dusty hall. There is a key on the floor, \
nearly hidden by the dust.',
    ),
    'Kitchen': Room(
        directions = {
            'north': 'Hall',
            'east': 'Garden',
        },
        monster = Monster(
            m_type = 'bear',
            health = 7,
            attack = 4,
            defence = 2,
            needs = [
                'potion'
            ],
            kill_text = 'The bear eats you.',
            killed_text = 'You killed the bear with a potion!',
        ),
        info = 'You are in a large kitchen. There is a bear here.',
    ),
    'Dining Room': Room(
        directions = {
            'west': 'Hall',
            'south': 'Garden',
        },
        items = [
            'potion',
        ],
        info = 'You are in a large dining room. There is a potion on the table.',
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

# A function to split an innput str into a list, with the first entry being
# the command, which may be multiple words
def parse_command(command: str):
    global commands
    for key in commands.keys():
        if command.startswith(key):
            if len(command) == len(key):
                return [key.strip()]
            return [key.strip()] + command[len(key):].strip().split()
    return False

def move(*directions):
    global player
    for direction in directions:
        if (rooms[player.current_room].directions and
            direction in rooms[player.current_room].directions):
            player.current_room = rooms[player.current_room].directions[direction]
        else:
            print(f'You can\'t go {direction}!')

def get(*items):
    global player
    # If the room contains an item, and the item is the one they want to
    # get
    for item in items:
        if (rooms[player.current_room].items and
            item in rooms[player.current_room].items):
            # Add the item to their inventory
            player.inventory.add(item)
            # Delete the item from the room
            del rooms[player.current_room].items[item]
        # Otherwise, if the item isn't there to get
        else:
            # Tell them they can't get it
            print('Can\'t get ' + item + '!')

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

def battle(player:Player, monster:Monster):
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

def handle_monster(room):
    global player
    monster = room.monster
    if type(monster) == Monster:
        if (monster.needs and
            all(x in player.inventory.items for x in monster.needs)):
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
            del room.monster
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
        "command": show_commands,
        "description": "Show the commands",
        "args": "number of commands to show. 0 to show all",
    },
}


def main():
    # Show the instructions
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

        command = parse_command(command)

        room = rooms[player.current_room]
        if type(room) == Room:
            if (room.exit and
                'needs' in rooms[player.current_room].exit):
                if all(x in player.inventory for x in rooms[player.current_room].exit.needs):
                    print('You escaped the house... YOU WIN!')
                    sys.exit()
                else:
                    print(
                        'You need ' +
                        ', '.join(rooms[player.current_room].exit.needs) +
                        ' to escape!'
                    )

            if command and len(command) >= 2:
                commands[command[0]]["command"](*command[1:])
            else:
                print('Invalid command!')
            
            room = rooms[player.current_room]

            if room.monster:
                handle_monster(room)

if __name__ == '__main__':
    main()
