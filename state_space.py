from state import State, StateType
import numpy as np
from action import Action

class StateSpace:

    def __init__(self,rows,columns,goal_1_position=(), goal_2_position=(), forbidden_position=(), wall_position=() ):
        # create an array to hold states
        self._space = np.empty(shape=(rows,columns), dtype="object")
        
        # create an array to hold the q values
        self._q_table = np.zeros(shape=(rows * columns,4))

        # fill the state space with empty state
        state_element_index = 0
        for i in range(0,rows):
            # create the state for this row
            for j in range (0,columns):
                # check what type of state we need to create based on location
                state_type = StateType.EMPTY
                if (i,j) == goal_1_position:
                    state_type = StateType.GOAL
                elif (i,j) == goal_2_position:
                    state_type = StateType.GOAL
                elif (i,j) == forbidden_position:
                    state_type = StateType.FORBIDDEN
                elif (i,j) == wall_position:
                    state_type = StateType.WALL

                # create the state    
                state = State(state_type=state_type)
                self._space[i,j] = state

        # num of times converged
        self._num_of_times_converged = 0
                
    def get_state(self,row,column):
        state = self._space[row][column]
        return state

    def get_shape(self):
        return self._space.shape

    # get the coordinates of the given state
    def get_coordinates(self,state):
        coordinates_array = np.where(self._space == state)
        coordinates = (coordinates_array[0][0], coordinates_array[1][0])
        return coordinates

    # get q value vector
    def get_q_value_vector(self):
        n_rows = self._space.shape[0] * self._space.shape[1] * 4
        q_values = np.empty(shape=(n_rows,1),dtype='float')
        state_space_flattened = self._space.flatten()
        index = 0
        for state in state_space_flattened:
            # add all the q values to q_values array
            q_values[index] = (state.get_value(Action.NORTH))
            index = index + 1
            q_values[index] = (state.get_value(Action.SOUTH))
            index = index + 1
            q_values[index] = (state.get_value(Action.EAST))
            index = index + 1
            q_values[index] = (state.get_value(Action.WEST))
            index = index + 1
            
        return q_values

    
    def has_converged(self,q_values_before, q_values_after):
        is_close = np.allclose(q_values_before,q_values_after)
        if is_close:
            self._num_of_times_converged = self._num_of_times_converged + 1
        else:
            self._num_of_times_converged = 0
        
        if self._num_of_times_converged > 10:
            return True
        else:
            return False

    def get_policy(self):
        # flatten the space
        flattened_space = self._space.flatten()
        policy = {}
        shape = self.get_shape()
        for state in flattened_space:
            coordinates = self.get_coordinates(state)
            position = StateSpace.to_position(coordinates)
            policy[str(position)] = state.get_best_action(coordinates,shape).value

        return policy

    @staticmethod
    def to_coordinates(position):
        row = int(position/4)
        column = int(position % 4) - 1
        if column == -1:
            column = 3
        return (row,column)

    @staticmethod
    def to_position(coordinates):
        row = coordinates[0]
        column = coordinates[1]
        position = (row * 4) + (column + 1)        
        return position

    def render(self):
        shape = self.get_shape()
        rows = shape[0]
        columns = shape[1]
        
        for i in range(0,rows):
            # create the state for this row
            for j in range (0,columns):
                position = StateSpace.to_position((i,j))
                state = self.get_state(i,j)
                render_item = position
                if state.get_type() == StateType.GOAL:
                    render_item = 'G'
                elif state.get_type() == StateType.FORBIDDEN:
                    render_item = 'F'
                elif state.get_type() == StateType.WALL:
                    render_item = 'W'

                print("{0:^5}".format(render_item),end='')

                if j == columns - 1:
                    print("\n")
