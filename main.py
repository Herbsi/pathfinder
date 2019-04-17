#!/usr/bin/env python3

import argparse
import sys

from dungeon import Dungeon, dungeon
from gamedata import GameData
from json_serialization import load_gamedata, save_gamedata
from player import Player
from village import Village, village


def print_bonus_tasks():
    # TODO: insert the tasks you implemented
    bonus_tasks = []
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
        gamedata = GameData(player=user, savefile=save, bonus_tasks=False)

    else:
        gamedata = load_gamedata(save)
        user = gamedata.player

    prog0 = Village(player=user, bonus_tasks=False)

    while True:
        user_choice = village(prog0)

        if user_choice == 5:
            dungeon(Dungeon(player=user, bonus_tasks=False))
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
    ui = input("Save before exiting? (Y/N) ")
    if ui.lower() in "y":
        save_gamedata(gamedata, savefile)


if __name__ == "__main__":
    main()
