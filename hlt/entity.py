import abc

from . import commands, constants
from .positionals import Direction, Position
from .common import read_input

class Entity(abc.ABC):
    """
    Base Entity Class from whence Ships, Dropoffs and Shipyards inherit
    """
    def __init__(self, owner, id, position):
        self.owner = owner
        self.id = id
        self.position = position

    @staticmethod
    def _generate(player_id):
        """
        Method which creates an entity for a specific player given input from the engine.
        :param player_id: The player id for the player who owns this entity
        :return: An instance of Entity along with its id
        """
        ship_id, x_position, y_position = map(int, read_input().split())
        return ship_id, Entity(player_id, ship_id, Position(x_position, y_position))

    def __repr__(self):
        return "{}(id={}, {})".format(self.__class__.__name__,
                                      self.id,
                                      self.position)

class Dropoff(Entity):
    """
    Dropoff class for housing dropoffs
    """
    pass

class Shipyard(Entity):
    """
    Shipyard class to house shipyards
    """
    def spawn(self):
        """Return a move to spawn a new ship."""
        return commands.GENERATE


class Ship(Entity):
    """
    Ship class to house ship entities
    """
    def __init__(self, owner, id, position, halite_amount):
        super().__init__(owner, id, position)
        self.halite_amount = halite_amount
        self.safe_moves = {}
        self.current_move = None
        self.moved = False

    @property
    def is_full(self):
        """Is this ship at max halite capacity?"""
        return self.halite_amount >= constants.MAX_HALITE

    def make_dropoff(self):
        """Return a move to transform this ship into a dropoff."""
        return "{} {}".format(commands.CONSTRUCT, self.id)

    def move(self, direction):
        """
        Return a move to move this ship in a direction without
        checking for collisions.
        """
        raw_direction = direction
        if not isinstance(direction, str) or direction not in "nsewo":
            raw_direction = Direction.convert(direction)
        return "{} {} {}".format(commands.MOVE, self.id, raw_direction)

    def set_moved(self, moved):
        self.moved = moved

    def get_current_move(self):
        return self.current_move

    def set_current_move(self, move):
        self.current_move = move

    def stay_still(self):
        """
        Don't move this ship.
        """
        return "{} {} {}".format(commands.MOVE, self.id, commands.STAY_STILL)

    def get_safe_moves(self):
        """
        Returns possible safe moves of this ship
        """
        return self.safe_moves

    def delete_safe_move(self, key):
        """
        Deletes a safe move
        """
        if key in self.safe_moves:
            del self.safe_moves[key]

    def pick_best_move(self):
        if bool(self.safe_moves) == False:
            return None
        else:
            return max(self.safe_moves, key=self.safe_moves.get)

    def set_safe_moves(self, moves):
        """
        Returns possible safe moves of this ship
        """
        self.safe_moves = moves

    @staticmethod
    def _generate(player_id):
        """
        Creates an instance of a ship for a given player given the engine's input.
        :param player_id: The id of the player who owns this ship
        :return: The ship id and ship object
        """
        ship_id, x_position, y_position, halite = map(int, read_input().split())
        return ship_id, Ship(player_id, ship_id, Position(x_position, y_position), halite)

    def __repr__(self):
        return "{}(id={}, {}, cargo={} halite, moved={})".format(self.__class__.__name__,
                                                       self.id,
                                                       self.position,
                                                       self.halite_amount,
                                                       self.moved)
