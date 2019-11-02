from enum import Enum
import random

class Action(Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"

    def get_allowed_action(coordinates,shape):

        if coordinates[0] == 0 and coordinates[1] == 0:
            return [
                Action.SOUTH,
                Action.EAST
            ]
        elif coordinates[0] == 0 and coordinates[1] == shape[1] - 1:
            return [
                Action.SOUTH,
                Action.WEST
            ]
        elif coordinates[0] == shape[0]-1 and coordinates[1] == 0:
            return [
                Action.NORTH,
                Action.EAST
            ]
        elif coordinates[0] == shape[0]-1 and coordinates[1] == shape[1] - 1:
            return [
                Action.NORTH,
                Action.WEST
            ]
        elif coordinates[0] == 0:
            return [
                Action.SOUTH,
                Action.WEST,
                Action.EAST
            ]
        elif coordinates[0] == shape[0]-1:
            return [
                Action.NORTH,
                Action.WEST,
                Action.EAST
            ]
        elif coordinates[1] == 0:
            return [
                Action.NORTH,
                Action.EAST,
                Action.SOUTH
            ]
        elif coordinates[1] == shape[1]-1:
            return [
                Action.NORTH,
                Action.WEST,
                Action.SOUTH
            ]
        else:
            return [
                Action.WEST,
                Action.NORTH,
                Action.EAST,
                Action.SOUTH
            ]
        