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
max_spawn_turn = 200
# max_spawn_turn = constants.MAX_TURNS - 200

# logging.info("max spawns: {}\n".format(max_spawn_turn))
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """

# total = 0

def fix_contention(game_map, command_queue, position):
    ship = game_map[position].get_ship()
    current_move = ship.get_current_move()
    ship.delete_safe_move(current_move)

    next_move = ship.pick_best_move()

    command_queue.remove(ship.move(current_move))
    command_queue.append(ship.move(next_move))

    game_map[position].mark_safe()

    if game_map[ship.position.directional_offset(next_move)].is_safe == False:
        logging.info("new move is unsafe")
        fix_contention(game_map, command_queue, ship.position.directional_offset(next_move))

while True:
    game.update_frame()
    me = game.me
    game_map = game.game_map

    command_queue = []

    direction_order = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]

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

            if game_map[position].is_enemy == False and game_map[position].is_safe == True:
                if direction == Direction.Still:
                    halite_dict[direction] = halite_amount * 3
                else:
                    halite_dict[direction] = halite_amount

        ship.set_safe_moves(halite_dict)

        if ship_states[ship.id] == "depositing":           
            moves = game_map.get_unsafe_moves(ship.position, me.shipyard.position)

            move = Direction.Still

            for potential_move in moves:
                position = position_dict[potential_move]

                if game_map[position].is_safe == True:
                    move = potential_move
                    break

            position = position_dict[move]

            if game_map[position].is_safe == False:
                logging.info("avoiding collision")
                fix_contention(game_map, command_queue, position)

            game_map[position].mark_unsafe(ship)
            ship.set_current_move(move)
            command_queue.append(ship.move(move))

            if move == Direction.Still and game_map.calculate_distance(ship.position, me.shipyard.position) == 0:
                ship_states[ship.id] = "collecting"

            if game_map.calculate_distance(position_dict[move], me.shipyard.position) + 2 >= constants.MAX_TURNS - game.turn_number:
                ship_states[ship.id] = "end"
        elif ship_states[ship.id] == "collecting":
            move = ship.pick_best_move()

            if move == None:
                move = Direction.Still

            position = position_dict[move]

            game_map[position].mark_unsafe(ship)
            ship.set_current_move(move)
            command_queue.append(ship.move(move))

            if ship.halite_amount > constants.MAX_HALITE * .75:
                ship_states[ship.id] = "depositing"

            if game_map.calculate_distance(position_dict[move], game_map[me.shipyard].position) + 2 >= constants.MAX_TURNS - game.turn_number:
                ship_states[ship.id] = "end"
        elif ship_states[ship.id] == "end":
            moves = game_map.get_unsafe_moves(ship.position, me.shipyard.position)
            distance = game_map.calculate_distance(ship.position, me.shipyard.position)

            move = Direction.Still

            for potential_move in moves:
                position = position_dict[potential_move]

                if game_map[position].is_occupied == False or distance == 1:
                    move = potential_move
                    break
            
            if distance > 1:
                position = position_dict[move]
                game_map[position].mark_unsafe(ship)
            
            ship.set_current_move(move)
            command_queue.append(ship.move(move))

    if game.turn_number <= max_spawn_turn and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_ally:
        game_map[me.shipyard.position].mark_unsafe(None)
        command_queue.append(me.shipyard.spawn())

    game.end_turn(command_queue)
