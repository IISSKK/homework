class Transport:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed

    def move(self):
        print(f"{self.name} движется со скоростью {self.speed} км/ч.")


class Car(Transport):
    def move(self):
        print(f"{self.name} едет по дороге.")

    def refuel(self):
        print(f"{self.name}: заправка топливом.")


class Bicycle(Transport):
    def move(self):
        print(f"{self.name} едет по велосипедной дорожке.")

    def ring_bell(self):
        print(f"{self.name}: дзынь-дзынь!")


class Airplane(Transport):
    def move(self):
        print(f"{self.name} летит в небе.")

    def take_off(self):
        print(f"{self.name}: взлёт.")



car = Car("Toyota", 120)
bike = Bicycle("Аист", 25)
plane = Airplane("Boeing 737", 850)


car.move()
bike.move()
plane.move()

print()


transports = [car, bike, plane]
for t in transports:
    t.move()

print()


car.refuel()
bike.ring_bell()
plane.take_off()
class Transport:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed

    def move(self):
        print(f"{self.name} движется со скоростью {self.speed} км/ч.")


class Car(Transport):
    def move(self):
        print(f"{self.name} едет по дороге.")

    def refuel(self):
        print(f"{self.name}: заправка топливом.")


class Bicycle(Transport):
    def move(self):
        print(f"{self.name} едет по велосипедной дорожке.")

    def ring_bell(self):
        print(f"{self.name}: дзынь-дзынь!")


class Airplane(Transport):
    def move(self):
        print(f"{self.name} летит в небе.")

    def take_off(self):
        print(f"{self.name}: взлёт.")


car = Car("Toyota", 120)
bike = Bicycle("Аист", 25)
plane = Airplane("Boeing 737", 850)

car.move()
bike.move()
plane.move()

print()


transports = [car, bike, plane]
for t in transports:
    t.move()

print()


car.refuel()
bike.ring_bell()
plane.take_off()