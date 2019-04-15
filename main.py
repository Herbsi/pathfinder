#!/usr/bin/env python3

import argparse
import sys

from gamedata import GameData
from json_serialization import load_gamedata, save_gamedata
from player import Player
from village import Village


def print_bonus_tasks():
    # TODO: insert the tasks you implemented
    bonus_tasks = []
    print(",".join(str(x) for x in bonus_tasks))


def main():
    parser = argparse.ArgumentParser(description="P0 Adventure")
    parser.add_argument(
        "--savefile", default="game.json", help="The save file. default: 'game.json'"
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

    if args.new_game:
        player = Player()
        player.create_new_character()

    Village({"player": player, "savefile": "", "bonus_tasks": False}).village()

    sys.exit(0)


if __name__ == "__main__":
    main()
