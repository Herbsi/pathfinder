#!/usr/bin/env python3

import argparse

from player import Player
from gamedata import GameData
from json_serialization import save_gamedata, load_gamedata

def print_bonus_tasks():
    # TODO: insert the tasks you implemented
    bonus_tasks = []
    print(','.join(str(x) for x in bonus_tasks))

def main():
    parser = argparse.ArgumentParser(description="P0 Adventure")
    parser.add_argument('--savefile', default="game.json",
        help="The save file. default: 'game.json'")
    parser.add_argument("--new-game", dest="new_game", default=False, action='store_true',
        help="Create a new save file.")
    parser.add_argument("-b", dest="bonus_tasks", default=False, action="store_true", help='enable bonus tasks')
    parser.add_argument("--print-bonus", dest="print_bonus", default=False, action="store_true", help='print bonus task list and exit')
    args = parser.parse_args( )

    if args.print_bonus:
        print_bonus_tasks()
        return

    # your code starts here

if __name__ == '__main__':
    main()
