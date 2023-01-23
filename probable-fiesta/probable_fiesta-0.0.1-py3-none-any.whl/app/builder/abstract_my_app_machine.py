from abc import ABC

class HotDrink(ABC):
    def consume(self):
        pass

class Tea(HotDrink):
    def consume(self):
        print("This tea is nice with lemon!")

class Coffee(HotDrink):
    def consume(self):
        print("This coffee is delicious!")

class HotDrinkFactory(ABC):
    def prepare(self, amount):
        pass

class TeaFactory(HotDrinkFactory):
    def prepare(self, amount):
        print(f"Put in tea bag, boil water, pour {amount}ml, add lemon, enjoy!")
        return Tea()

class CoffeeFactory(HotDrinkFactory):
    def prepare(self, amount):
        print(f"Grind some beans, boil water, pour {amount}ml, add cream and sugar, enjoy!")
        return Coffee()

class HotDrinkMachine:
    class AvailableDrink:
        COFFEE = 0
        TEA = 1

    initializers = [CoffeeFactory, TeaFactory]

    def __init__(self):
        self.factories = [initializer() for initializer in self.initializers]

    def make_drink(self):
        print("Available drinks:")
        for f in range(len(self.factories)):
            print(f"{f}: {self.factories[f]}")

        idx = int(input(f"Please pick drink (0-{len(self.factories)-1}): "))
        amount = int(input("Specify amount: "))
        return self.factories[idx].prepare(amount)

    def make_drink(self, drink, amount):
        return self.factories[drink].prepare(amount)

def make_drink(type):
    if type == HotDrinkMachine.AvailableDrink.TEA:
        return TeaFactory().prepare(200)
    elif type == HotDrinkMachine.AvailableDrink.COFFEE:
        return CoffeeFactory().prepare(50)
    else:
        print("Incorrect drink type")

def create_sample_drink():
    hdm = HotDrinkMachine()
    drink = hdm.make_drink()
    drink.consume()

