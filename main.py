#!/usr/bin/env python3

import argparse
import sys

import helpers
from chest import Chest
from dungeon import Dungeon
from gamedata import GameData
from gravedigger import Gravedigger
from json_serialization import load_gamedata, save_gamedata
from player import Player
from shopkeeper import Shopkeeper, blacksmith_items, druid_items
from village import Village


def print_bonus_tasks():
    # TODO: insert the tasks you implemented
    bonus_tasks = ["gravedigger"]
    print(",".join(str(x) for x in bonus_tasks))


def main():
    parser = argparse.ArgumentParser(description="P0 Adventure")
    parser.add_argument(
        "--savefile",
        dest="savefile",
        default="game.json",
        help="The save file. default: 'game.json'",
    )
    parser.add_argument(
        "--new-game",
        dest="new_game",
        default=False,
        action="store_true",
        help="Create a new save file.",
    )
    parser.add_argument(
        "-b",
        dest="bonus_tasks",
        default=False,
        action="store_true",
        help="enable bonus tasks",
    )
    parser.add_argument(
        "--print-bonus",
        dest="print_bonus",
        default=False,
        action="store_true",
        help="print bonus task list and exit",
    )
    args = parser.parse_args()

    if args.print_bonus:
        print_bonus_tasks()
        return

    # your code starts here
    save = args.savefile
    if args.new_game:
        user = Player()
        user.createNewCharacter()
        gamedata = GameData(player=user, savefile=save, bonus_tasks=args.bonus_tasks)

    else:
        gamedata = load_gamedata(save)
        user = gamedata.player

    schmied = Shopkeeper(name="blacksmith", inventory=blacksmith_items)
    druide = Shopkeeper(name="druid", inventory=druid_items)
    prog0 = Village(
        player=user, bonus_tasks=args.bonus_tasks, blacksmith=schmied, druid=druide
    )

    if args.bonus_tasks:
        totengraeber = Gravedigger()
        prog0.gravedigger = totengraeber

        truhe = Chest()
        prog0.chest = truhe

    while True:
        user_choice = village(prog0)

        if user_choice == 5:
            dung0 = Dungeon(player=user, bonus_tasks=args.bonus_tasks)
            if args.bonus_tasks:
                dung0.gravedigger = totengraeber
            dungeon(dung0)
        elif user_choice == 6:
            save_gamedata(gamedata, save),
            print("Game saved to {}".format(save))
        elif user_choice == 0:
            quit(gamedata, save)
            break
        else:
            raise KeyError(
                "main.py Something went wrong with the user choosing what to do!"
            )

    sys.exit(0)


def quit(gamedata, savefile):
    user_input = input("Save before exiting? (Y/N) ")
    if user_input.lower() in "y":
        save_gamedata(gamedata, savefile)


def village(vill):
    option_count = 7 if not vill.bonus_tasks else 9

    def pre():
        print("Welcome to Prog0 Village!")
        print("What do you want to do?")
        print()
        print("  1) Inventory")
        print("  2) Merchant")
        print("  3) Blacksmith")
        print("  4) Druid")
        print("  5) Dungeon")
        print("  6) Save game")
        if vill.bonus_tasks:
            print("  7) Gravedigger")
            print("  8) Treasure Chest")
        print("  0) Quit game")
        print()

    while True:
        if vill.player.isdead:
            vill.player.revive()

        user_input = helpers.validInput(
            "> ",
            "Invalid choice. Try again.",
            lambda x: x in range(option_count),
            preamble=pre,
            cast=int,
        )

        if user_input in [0, 5, 6]:
            return user_input

        vill.village_dict[user_input]()


def dungeon(dung):
    option_count = 6 if not dung.bonus_tasks else 6

    dung.lookAround()

    def pre():
        print("What do you want to do?")
        print()
        print("  1) Inventory")
        print("  2) Look Around")
        print("  3) Attack")
        print("  4) Open chest")
        print("  5) Move")
        if dung.bonus_tasks:
            pass
        print("  0) Run away (leave dungeon)")
        print()

    while True:
        if dung.player.isdead:
            return

        user_input = 0

        user_input = helpers.validInput(
            "> ",
            "Invalid choice. Try again.",
            lambda x: x in range(option_count),
            preamble=pre,
            cast=int,
        )

        if user_input == 0:
            return

        dung.dungeon_dict[user_input]()


if __name__ == "__main__":
    main()
