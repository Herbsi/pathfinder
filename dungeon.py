import helpers
from item import Item
from json_serialization import json_class
from monster import Monster
from player import Player


def dungeon(dung):
    dung.lookAround()
    while True:
        if dung.player.isdead:
            return
        user_input = 0

        def pre():
            print("What do you want to do?")
            print()
            print("  1) Inventory")
            print("  2) Look Around")
            print("  3) Attack")
            print("  4) Open chest")
            print("  5) Move")
            print("  6) Run away (leave dungeon)")
            print()

        user_input = helpers.validInput(
            "> ",
            "Invalid choice. Try again.",
            lambda x: x in range(1, 7),
            preamble=pre,
            cast=int)


        dung.dungeon_dict[user_input]()
        if user_input == 6:
            return user_input


@json_class
class Dungeon:
    def __init__(self, player, bonus_tasks):
        self.player = player
        self.monsters = [
            self.possibleMonsters["Rat"], self.possibleMonsters["Gnoll"]
        ]
        self.room = 1
        self.bonus_tasks = bonus_tasks

    @property
    def dungeon_dict(self):
        return {
            1: self.player.listInventory,
            2: self.lookAround,
            3: self.attack,
            4: self.openChest,
            5: self.move,
        }

    @property
    def possibleMonsters(self):
        return {
            "Rat":
            Monster(
                name="Rat",
                health=30,
                attack=10,
                defense=15,
                speed=50,
                reward_min=1,
                reward_max=5),
            "Gnoll":
            Monster(
                name="Gnoll",
                health=60,
                attack=30,
                defense=40,
                speed=20,
                reward_min=5,
                reward_max=10),
            "Wolf":
            Monster(
                name="Wolf",
                health=40,
                attack=25,
                defense=30,
                speed=60,
                reward_min=10,
                reward_max=15)
        }

    def lookAround(self):
        # TODO create list of random descriptions that are displayed
        description = "nothing"
        print("You see {}".format(description))

    def attack(self):
        if not self.monsters:
            print("You are alone in this room.")
            return

        while True:
            if self.player.isdead:
                return
            elif not self.monsters:
                print("All enemies defeated")
                return
            self.battleRound()

    def move(self):
        if not self.monsters:
            self.room += 1
            self.newRoom()
        else:
            print("Monsters are blocking your way.")

    def openChest(self):
        if not self.monsters:
            if not self.chest:
                print("The chest is empty.")
            else:
                for item in self.chest:
                    self.player.addItem(item)
                    print(
                        "You collected {0.name} from the chest.".format(item))
        else:
            print("Monsters are blocking your way.")

    # def run_away(self):
    #     return

    def newRoom(self):
        if self.room % 2 == 1:
            self.monsters = [
                self.possibleMonsters["Rat"], self.possibleMonsters["Gnoll"]
            ]
            self.chest = []
        else:
            self.monsters = [
                self.possibleMonsters["Wolf"], self.possibleMonsters["Rat"]
            ]
            self.chest = [
                Item(
                    name="Potion",
                    price=3,
                    influenced_attribute="health",
                    amount=10)
            ]

    def battleRound(self):
        attackers = (self.player, *self.monsters)
        attackers = sorted(
            attackers, key=lambda creature: creature.speed, reverse=True)
        monster_index = self.playerChooseMonster() - 1
        for attacker in attackers:
            if isinstance(attacker, Player):
                defender = self.monsters[monster_index]
                dmg = damage(self.player, defender)
                defender.health -= dmg
                print("You attacked {0.name} and dealt {1} damage.".format(
                    defender, dmg))
                if defender.health < 1:
                    print("{0.name} died. It dropped {0.reward} gold".format(
                        defender))
                    self.player.gold += defender.reward
                    self.monsters.remove(defender)

            elif isinstance(attacker, Monster):
                dmg = damage(attacker, self.player)
                self.player.health -= dmg
                print("{0.name} attacked you and dealt {1} damage.".format(
                    attacker, dmg))
                if self.player.isdead:
                    print("You were killed by {0.name}".format(attacker))
                    self.player.die()
                    return

    def playerChooseMonster(self):
        monster_count = len(self.monsters)

        def pre():
            print("You see the following enemies:")
            print()
            for index, monster in enumerate(self.monsters):
                print("  {idx}) {mons.name:<20} ({mons.health} HP)".format(
                    idx=index + 1, mons=monster))

            print()
            print("You have {} health.".format(self.player.health))
            print("Which enemy would you like to attack?")

        return helpers.validInput(
            "> ",
            "Please input a positive integer between 1 and {}",
            lambda x: x in range(1, monster_count + 1),
            monster_count,
            preamble=pre,
            cast=int)


def damage(attacker, defender):
    return (attacker.attack**2) // (attacker.attack + defender.defense)
