from item import Item
from json_serilization import json_class
from monster import Monster
from player import Player


@json_class
class Dungeon:
    def __init__(self, player, bonus_tasks):
        self.player = player
        self.monsters = []
        self.room = 1
        self.bonus_tasks = bonus_tasks

    def dungeon(self):
        while True:
            user_input = 0
            self.look_around()
            while True:
                print("What do you want to do?")
                print()
                print("  1) Inventory")
                print("  2) Look Around")
                print("  3) Attack")
                print("  4) Open chest")
                print("  5) Move")
                print("  6 Run away Leave dungeon")

                try:
                    user_input = int(input(" >"))
                    if user_input in range(1,7):
                        break
                except ValueError:
                    pass

                print("Invalid choice. Try again.")

            self.dungeon_dict[user_input]()
            if user_input == 6:
                return

    @property
    def dungeon_dict(self):
        return {
            1: self.player.list_inventory,
            2: self.look_around,
            3: self.attack,
            4: self.open_chest,
            5: self.move,
            6: self.run_away
        }

    @property
    def possibleMonsters(self):
        return {
            "Rat"   : Monster(name="Rat"   , health=30 , attack=10 , defense=15 , speed = 50 , reward_min=1  , reward_max=5)  ,
            "Gnoll" : Monster(name="Gnoll" , health=60 , attack=30 , defense=40 , speed=20   , reward_min=5  , reward_max=10) ,
            "Wolf"  : Monster(name="Wolf"  , health=40 , attack=25 , defense=30 , speed=60   , reward_min=10 , reward_max=15)
            }


    def look_around(self):
        # TODO create list of random descriptions that are displayed
        description = "nothing"
        print("You see {}".format(description))

    def attack(self):
        if self.monsters:
            while True:
                if not self.monsters:
                    print("All enemies defeated.")
                self.battleRound()
        print("You are alone in this room.")

    def move(self):
        if not self.monsters:
            self.room += 1
            self.new_room()
        else:
            print("Monsters are blocking your way.")

    def openChest(self):
        if not self.monsters:
            if not self.chets:
                print("The chest is empty.")
            else:
                for item in self.chest:
                    self.player.addItem(item)
                    print("You collected {0.name} from the chest.".format(item))
        else:
            print("Monsters are blocking your way.")



    def run_away(self):
        return

    def new_room(self):
        if self.room % 2 == 1:
            self.monsters = [self.possibleMonsters["Rat"], self.possibleMonsters["Gnoll"]]
            self.chest = []
        else:
            self.monsters = [self.possibleMonsters["Wolf"], self.possibleMonsters["Rat"]]
            self.chest = [Item(name="Potion", price=3, influenced_attribute="health", amount=10)]

    def battleRound(self):
        attackers = [self.player].extend(self.monsters)
        attackers = sorted(attackers, key=lambda creature : creature.speed, reverse=True)
        for attacker in attackers:
            if isinstance(attacker, Player):
                monster_index = self.playerChooseMonster(self)
                defender = self.monsters[monster_index]
                damage = self.damage(self.player, defender)
                defender.health -= damage
                print("You attacked {0.name} and dealt {1} damage.".format(defender, damage))
                if defender.health < 1:
                    print("{0.name} died. It dropped {0.reward} gold".format(defender))
                    self.player.gold += defender.reward

            elif isinstance(attacker, Monster):
                damage = self.damage(attacker, self.player)
                self.player.health -= damage
                print("{0.name} attacked you and dealt {1} damage.".format(attacker, damage))
                if self.player.health < 1:
                    print("You were killed by {0.name}".format(attacker))
                    self.player.die()
                    # TODO return to village



    def damage(attacker, defender):
        return (attacker.attack ** 2) // (attacker.attack + defender.defense)

    def playerChooseMonster(self):
        print("You see the following enemies:")
        print()
        for index, monster in self.monsters:
            print("  {idx}) {mons.name:<20} (mons.health HP)".format(idx=index+1, mons=monster))

        print()
        print("You have {} health.".format(self.player.health))
        print("Which enemy would you like to attack?")
        try:
            user_input = int(input("> "))
            if user_input in range(1, len(self.monsters)):
                return user_input
        except ValueError:
            pass
        print("Please input a positive integer between 1 and {}".format(len(self.monsters)))
