from . import utils as u

class Item:
    def __init__(self, name, size=1.0):
        self.name = name
        self.size = size


class Inventory:
    def __init__(self):
        self.items = []
        self.size = 10.0

    def add(self, item):
        used_size = sum(item.size for item in self.items)
        if used_size + item.size <= self.size:
            self.items.append(item)
            print(f'{item.name} got!')
            return True
        else:
            print(f'Not enough space to add {item.name}!')
            return False

    def has(self, item):
        return any(i.name == item for i in self.items)
    
    def find(self, item):
        # Finds an item in the inventory and returns the item object
        # or None if not found, and also returns the index of the item in the
        # inventory This is used to remove the item from the inventory
        if self.has(item):
            for i in self.items:
                if i.name == item:
                    return i, self.items.index(i)
        return None, None

    def remove(self, item):
        if type(item) == Item:
            item = item.name
        i, itemplace = self.find(item)
        u.DEBUG(i, itemplace)
        if i:
            self.items.remove(i)
            return True
        return False

    def __str__(self):
        inventory = ', '.join(item.name for item in self.items)
        if inventory == '':
            inventory = 'empty'
        som = sum(item.size for item in self.items)
        used_size = som if som > 0 else 0.0
        inventory += f' ({used_size}/{self.size})'
        return inventory
