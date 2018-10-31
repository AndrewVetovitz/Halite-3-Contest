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
end_moves_offset = 10
# max_spawn_turn = constants.MAX_TURNS - 200

# logging.info("max spawns: {}\n".format(max_spawn_turn))
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """

# total = 0

while True:
    game.update_frame()
    me = game.me
    game_map = game.game_map

    command_queue = []

    direction_order = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]

    for ship in me.get_ships():
        # Setting new ship states to collecting
        if ship.id not in ship_states:
            ship_states[ship.id] = "collecting"

    for ship in me.get_ships():
        if ship.moved == True:
            continue

        # If ship cannot move due to insufficent halite
        if ship.halite_amount < int(0.1 * game_map[ship.position].halite_amount):
            ship.set_current_move(Direction.Still)
            ship.set_moved(True)
            game_map[ship.position].mark_unsafe(ship)

    for ship in me.get_ships():
        if ship.moved == True:
            continue

        # Moving all depositors back to base
        if ship_states[ship.id] == "depositing": 
            position_options = ship.position.get_surrounding_cardinals() + [ship.position]

            position_dict = {}
            move_dict = {}

            for n, direction in enumerate(direction_order):
                position_dict[direction] = position_options[n]

            for direction in position_dict:
                position = position_dict[direction]
                distance = game_map.calculate_distance(position, me.shipyard.position)

                if game_map[position].is_safe == True and (game_map[position].is_enemy == False or position == me.shipyard.position):
                    move_dict[direction] = distance + game_map[position].halite_amount / 1000

            move = min(move_dict, key=move_dict.get)
            position = position_dict[move]

            if game_map[position].is_safe == False:
                logging.info("depositing unsafe needs to move id={} move={}".format(ship.id, move))

            ship.set_current_move(move)
            ship.set_moved(True)
            game_map[position].mark_unsafe(ship)

            if game_map.calculate_distance(ship.position, me.shipyard.position) == 0:
                ship_states[ship.id] = "collecting"

            if game_map.calculate_distance(position_dict[move], me.shipyard.position) + end_moves_offset >= constants.MAX_TURNS - game.turn_number:
                ship_states[ship.id] = "end"

    for ship in me.get_ships():
        if ship.moved == True:
            continue

        # Moving all collectors
        if ship_states[ship.id] == "collecting":
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

            move = ship.pick_best_move()

            if move == None:
                move = Direction.Still

            position = position_dict[move]

            if game_map[position].is_safe == False:
                logging.info("collecting unsafe needs to move id={} move={}".format(ship.id, move))

            ship.set_current_move(move)
            ship.set_moved(True)
            game_map[position].mark_unsafe(ship)

            if ship.halite_amount == constants.MAX_HALITE:
                ship_states[ship.id] = "depositing"

            if game_map.calculate_distance(position_dict[move], me.shipyard.position) + end_moves_offset >= constants.MAX_TURNS - game.turn_number:
                ship_states[ship.id] = "end"

    for ship in me.get_ships():
        if ship.moved == True:
            continue

        # Moving all end
        if ship_states[ship.id] == "end":
            position_options = ship.position.get_surrounding_cardinals() + [ship.position]

            position_dict = {}
            move_dict = {}

            for n, direction in enumerate(direction_order):
                position_dict[direction] = position_options[n]

            for direction in position_dict:
                position = position_dict[direction]
                distance = game_map.calculate_distance(position, me.shipyard.position)

                if distance == 0 or (game_map[position].is_enemy == False and game_map[position].is_safe == True):
                    move_dict[direction] = distance

            if bool(move_dict) == True:
                move = min(move_dict, key=move_dict.get)
            else:
                move = Direction.Still
            
            position = position_dict[move]
            dist = game_map.calculate_distance(position, me.shipyard.position)

            if game_map[position].is_safe == False:
                logging.info("end unsafe move id={} move={}".format(ship.id, move))
                # copy_pos = position

                # contender = game_map[copy_pos].ship

                # while contender is not None:
                #     contender.set_current_move(Direction.Still)
                #     copy_pos = contender.position
                #     contender_next = game_map[copy_pos].ship
                #     game_map[copy_pos].mark_unsafe(contender)
                #     contender = contender_next

            if dist > 0:
                game_map[position].mark_unsafe(ship)
            
            ship.set_moved(True)
            ship.set_current_move(move)

    for ship in me.get_ships():
        # Puts ship moves into command queue
        if ship.moved == False:
            logging.info("Ship issued no move order id={}".format(ship.id))
            ship.set_current_move(Direction.Still)

        move = ship.current_move

        command_queue.append(ship.move(move))

    if game.turn_number <= max_spawn_turn and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_ally and game_map[me.shipyard].is_safe:
        game_map[me.shipyard.position].mark_unsafe(None)
        command_queue.append(me.shipyard.spawn())

    game.end_turn(command_queue)
