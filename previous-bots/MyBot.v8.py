#!/usr/bin/env python3
# Python 3.6
import hlt
from hlt import constants
from hlt.positionals import Direction

import sys
import random
import logging

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()

version = sys.argv[0].split(".")[1]
game.ready("Pink Bot {}".format(version))

ship_states = {}

logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """

while True:
    game.update_frame()
    me = game.me
    game_map = game.game_map

    command_queue = []

    direction_order = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]
    position_choices = []

    for ship in me.get_ships():
        if ship.id not in ship_states:
            ship_states[ship.id] = "collecting"

        position_options = ship.position.get_surrounding_cardinals() + [ship.position]

        position_dict = {}
        halite_dict = {}

        for n, direction in enumerate(direction_order):
            position_dict[direction] = position_options[n]

        for direction in position_dict:
            position = position_dict[direction]
            halite_amount = game_map[position].halite_amount

            if position_dict[direction] not in position_choices:
                if direction == Direction.Still:
                    halite_dict[direction] = halite_amount * 3
                else:
                    halite_dict[direction] = halite_amount

        if ship_states[ship.id] == "depositing":           
            diff = ship.position - me.shipyard.position

            if diff.x > 0 and position_dict[Direction.West] not in position_choices:
                move = Direction.West
            elif diff.x < 0 and position_dict[Direction.East] not in position_choices:
                move = Direction.East
            elif diff.y > 0 and position_dict[Direction.North] not in position_choices:
                move = Direction.North
            elif diff.y < 0 and position_dict[Direction.South] not in position_choices:
                move = Direction.South
            else:
                move = Direction.Still

            position_choices.append(position_dict[move])
            command_queue.append(ship.move(move))

            if move == Direction.Still and diff.x == 0 and diff.y == 0:
                ship_states[ship.id] = "collecting"
        elif ship_states[ship.id] == "collecting":
            move = max(halite_dict, key=halite_dict.get)

            position_choices.append(position_dict[move])
            command_queue.append(ship.move(move))

            if ship.halite_amount > constants.MAX_HALITE * .85:
                ship_states[ship.id] = "depositing"

    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied and game_map[me.shipyard].position not in position_choices:
        command_queue.append(me.shipyard.spawn())

    game.end_turn(command_queue)
