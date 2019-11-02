from enum import Enum
from action import Action
import random

'''
Enum to hold the type of cell
'''
class StateType(Enum):
    WALL = 1
    GOAL = 2
    FORBIDDEN = 3
    EMPTY = 4


'''
Class representing individual cell on the grid
'''
class State:
    
    def __init__(self,state_type):
        self._state_type=state_type
        self._q_table = {
            Action.NORTH : 0,
            Action.EAST : 0,
            Action.WEST: 0,
            Action.SOUTH: 0
        }
        self._utility = 0
    
    def get_value(self,action):
        return self._q_table[action]
    
    def get_values(self):
        return self._q_table

    def set_value(self,action, value):
        self._q_table[action] = value

    def get_type(self):
        return self._state_type
        

    def get_best_action(self,coordinates, shape):
        highest_value = -10000000000
        selected_actions = []
        allowed_actions = Action.get_allowed_action(coordinates,shape)
        for action in allowed_actions:
            value = self._q_table[action]
            # if this was the highest value yet, then clear all the items in selected action
            if value > highest_value:
                selected_actions.clear()
                highest_value = value
                selected_actions.append(action)

            # if the value was equal to previous selected values, then append the action to list
            elif value == highest_value:
                selected_actions.append(action)
        
        # choose from the action list randomly as this list contains values that are all equal
        return random.choice(selected_actions)
            

    def get_random_action(self, coordinates, shape):
        allowed_actions = Action.get_allowed_action(coordinates,shape)
        return random.choice(allowed_actions)

            
    def get_utility(self):
        if self.get_type() == StateType.GOAL:
            return 100
        elif self.get_type() == StateType.EMPTY:
            return self._utility
        elif self.get_type() == StateType.FORBIDDEN:
            return -100
        elif self.get_type() == StateType.WALL:
            return 0

    def set_utility(self,value):
        self._utility = value

    def get_max_value(self):
        highest_value = 0
        for key, value in self._q_table.items():
            # if this was the highest value yet, then clear all the items in selected action
            if value >= highest_value:
                highest_value = value
        
        return highest_value

    def __str__(self):
        return str(self._utility)

    def __repr__(self):
        return """**N:{:.2f} W:{:.2f} '\033[1m'{:.2f}'\033[0m' S:{:.2f} E:{:.2f}**""".format(self.get_value(Action.NORTH),
                                                                                             self.get_value(Action.WEST),
                                                                                             self.get_utility(),
                                                                                             self.get_value(Action.SOUTH),
                                                                                             self.get_value(Action.EAST))
        #return "{:.2f}".format(self.get_utility())