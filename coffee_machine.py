class CoffeeMachine:
    state = "exit"
    resources = {"water": 0,
                 "milk": 0,
                 "coffee": 0,
                 "cups": 0}
    money = 0
    coffee_types = [{"water": 250,
                     "milk": 0,
                     "coffee": 16,
                     "cups": 1,
                     "money": 4},
                    {"water": 350,
                     "milk": 75,
                     "coffee": 20,
                     "cups": 1,
                     "money": 7},
                    {"water": 200,
                     "milk": 100,
                     "coffee": 12,
                     "cups": 1,
                     "money": 6}]

    def __init__(self):
        self.resources["water"] = 400
        self.resources["milk"] = 540
        self.resources["coffee"] = 120
        self.resources["cups"] = 9
        self.money = 550
        self.start()

    def start(self):
        print("Write action (buy, fill, take, remaining, exit):")
        self.state = "action"

    def buy(self, action):
        if self.state == "buy":
            print()
            print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")
            self.state = "buy_coffee_type"
        elif self.state == "buy_coffee_type":
            if action == "back":
                print()
                self.start()
            elif not action.isdigit():
                print("Correct input must be integer! Please try again:")
            elif (int(action) - 1 > len(self.coffee_types)) or (int(action) <= 0):
                print(f"Correct input must be 1..{len(self.coffee_types)}! Please try again:")
            else:
                for resource in self.resources.keys():
                    if self.resources[resource] < self.coffee_types[int(action) - 1][resource]:
                        print(f"Sorry, not enough {resource}!")
                        break
                else:
                    for resource in self.resources.keys():
                        self.resources[resource] -= self.coffee_types[int(action) - 1][resource]
                    self.money += self.coffee_types[int(action) - 1]["money"]
                    print("I have enough resources, making you a coffee!")

                print()
                self.start()

    def fill(self, action):
        if self.state == "fill":
            print()
            print("Write how many ml of water do you want to add:")
            self.state = "fill_water"
        elif self.state == "fill_water":
            self.resources["water"] += int(action)
            print("Write how many ml of milk do you want to add:")
            self.state = "fill_milk"
        elif self.state == "fill_milk":
            self.resources["milk"] += int(action)
            print("Write how many ml of coffee beans do you want to add:")
            self.state = "fill_coffee"
        elif self.state == "fill_coffee":
            self.resources["coffee"] += int(action)
            print("Write how many disposable cups of coffee do you want to add:")
            self.state = "fill_cups"
        elif self.state == "fill_cups":
            self.resources["cups"] += int(action)
            print()
            self.start()

    def take(self):
        print(f"I gave you ${self.money}")
        print()
        self.start()
        self.money = 0

    def remaining(self):
        print(f"The coffee machine has:")
        print(f"{self.resources['water']} of water")
        print(f"{self.resources['milk']} of milk")
        print(f"{self.resources['coffee']} of coffee beans")
        print(f"{self.resources['cups']} of disposable cups")
        print(f"{self.money} of money")
        print()
        self.start()

    def action(self, action):
        if self.state == "action":
            if action == "buy":
                self.state = "buy"
                self.buy(action)
            elif action == "fill":
                self.state = "fill"
                self.fill(action)
            elif action == "take":
                self.take()
            elif action == "remaining":
                self.remaining()
            elif action == "exit":
                self.state = "exit"
        elif self.state.startswith("fill"):
            self.fill(action)
        elif self.state.startswith("buy"):
            self.buy(action)


machine = CoffeeMachine()
while machine.state != "exit":
    machine.action(input("> "))
