import random
import sys
from . import items
from . import utils as u
from . import event as e
# This file contains the classes for the beings in the game.
# The Player class and the Monster class are subclasses of the Being class.

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
    def __init__(
            self,
            m_type,
            health,
            attack,
            defence,
            needs=None,
            kill_text='',
            killed_text='',
            destroy_needs=True,
        ):
        super().__init__(health, attack, defence, m_type)
        self.type = m_type
        self.needs = needs or []
        self.kill_text = kill_text
        self.killed_text = killed_text
        self.destroy_needs = destroy_needs

class Player(Being):
    def __init__(
            self,
            current_room,
            last_room,
            health,
            attack,
            defence,
            name,
            inventory:items.Inventory = items.Inventory(),
            XP=0,
            LVL=1
        ):
        super().__init__(health, attack, defence, name)
        self.current_room = current_room
        self.last_room = last_room
        self.inventory = inventory
        self.XP = XP
        self.level = LVL
        self.deaths = 0
        self.max_health = health
    
    def die(self):
        self.deaths += 1
        print(f'You died! You have died {self.deaths} times!')
        shouldrickroll = input('Do you want to rewind time (for a price)? yes/no: ').strip().lower().startswith('y')
        if shouldrickroll:
            u.rickroll(self.deaths)
            self.health = self.max_health
            self.current_room = self.last_room
        else:
            super().die()
