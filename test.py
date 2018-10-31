#!/usr/bin/env python3
# Python 3.6
import hlt
from hlt import constants
from hlt.positionals import Direction, Position

import sys
import random
import logging

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()

version = ""
game.ready("Pink Bot {}".format(version))

ship_states = {}
max_spawn_turn = 200
# max_spawn_turn = constants.MAX_TURNS - 200

# logging.info("max spawns: {}\n".format(max_spawn_turn))
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

        move = Direction.Still
        command_queue.append(ship.move(move))

        for h in range(game_map.height):
            for w in range(game_map.width):
                game_map[Position(h, w)].halite_amount

    # logging.info(position_choices)

    # logging.info(game_map[me.shipyard].position)

    # if game.turn_number <= max_spawn_turn and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied and game_map[me.shipyard].position not in position_choices:
    #     command_queue.append(me.shipyard.spawn())

    game.end_turn(command_queue)
