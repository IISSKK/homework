class Character:
    def __init__(self, name, health=100, damage=10):
        self.name = name
        self.health = health
        self.damage = damage

    def attack(self):
        print(f"{self.name} совершает атаку.")

    def show_info(self):
        print(f"Имя: {self.name}, Здоровье: {self.health}, Урон: {self.damage}")

class Warrior(Character):
    def __init__(self, name, health=100, damage=30):
        super().__init__(name, health, damage)

    def attack(self):
        super().attack()
        print(f"{self.name} использует удар мечом и наносит {self.damage} урона.")

class Mage(Character):
    def __init__(self, name, health=100, damage=40):
        super().__init__(name, health, damage)

    def attack(self):
        super().attack()
        print(f"{self.name} использует заклинание и наносит {self.damage} урона.")

class Archer(Character):
    def __init__(self, name, health=100, damage=20):
        super().__init__(name, health, damage)

    def attack(self):
        super().attack()
        print(f"{self.name} стреляет из лука и наносит {self.damage} урона.")

warrior1 = Warrior(name='Артем', health=100, damage=30)
mage1 = Mage(name='Айпери', health=100, damage=40)
archer1 = Archer(name='Азамат', health=100, damage=20)

characters = [warrior1, mage1, archer1]

for char in characters:
    char.show_info()
    char.attack()
    print("-" * 35)