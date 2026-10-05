# Write your code here :-)
class Computer:
    def __init__(self, model, memory, disk_storage, cost):
        self.model = model
        self.memory = memory
        self.disk_storage = disk_storage
        self.cost = cost

    def description (self):
        print(f'Model: {self.model}')
        print(f'Memory: {self.memory}')
        print(f'Disk {self. disk_storage}')
        print(f'Cost: ${self.cost}')

my_pc = Computer('HP Envy 16', 16, '1TB SSD', 1399.99)
my_pc .description()