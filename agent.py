import random
from action import Action
from state import StateType

class Agent:

    def __init__(self, state_space, start_state, learning_rate,discount_rate, exploit_prob, living_reward):
        self._state_space = state_space
        self._current_state = start_state
        self._learning_rate = learning_rate
        self._discount_rate = discount_rate
        self._exploit_prob = exploit_prob
        self._living_reward = living_reward

    def set_start_state(self,start_state):
        self.start_state = start_state

    def set_exploit_prob(self, value):
        self._exploit_prob = value

    # perform the step
    def step(self):
        # choose the next action to perform in the current state
        action = self.get_action(self._current_state)
                
        # get the next state based on this action
        next_state = self.get_next_state(action, self._current_state)
                
        # check if the current state is goal state
        is_goal = False
        if next_state.get_type() == StateType.GOAL:
                        
            # calculate the new q value for this state and action
            previous_q_value = self._current_state.get_value(action)
            
            # goal state the agent gets reward of 100
            reward = 100 + self._living_reward

            # update the q value
            q_value = ((1-self._learning_rate)*previous_q_value) + self._learning_rate * (reward + (self._discount_rate * next_state.get_max_value()))
            
            # set the new q value for the current state
            self._current_state.set_value(action,q_value)

            # calculate the utility for current state
            utility = next_state.get_utility() + self._living_reward
            self._current_state.set_utility(utility) 

            # update the current state
            self._current_state = next_state

            is_goal = True

        elif next_state.get_type() == StateType.FORBIDDEN:
                        
            # calculate the new q value for this state and action
            previous_q_value = self._current_state.get_value(action)
            
            # for forbidden a reward of -100
            reward = -100 + (self._living_reward)

            # update the q value
            q_value = ((1-self._learning_rate)*previous_q_value) + self._learning_rate * (reward + (self._discount_rate * next_state.get_max_value()))
            
            # set the new q value for the current state
            self._current_state.set_value(action,q_value)

            # update the current state
            self._current_state = next_state
            
            is_goal = False

        elif next_state.get_type() == StateType.WALL:
            # calculate the new q value for this state and action
            previous_q_value = self._current_state.get_value(action)
            
            # for wall you don't get reward but just a living reward for making a move
            reward = 0 + self._living_reward

            # update the q value
            q_value = ((1-self._learning_rate)*previous_q_value) + self._learning_rate * (reward + (self._discount_rate * next_state.get_max_value()))
            
            # no state updating, try again staying in the current state


            is_goal = False

        elif next_state.get_type() == StateType.EMPTY:
                        
            # calculate the new q value for this state and action
            previous_q_value = self._current_state.get_value(action)
            
            # calulcate the reward for this state
            reward = 1 + self._living_reward

            # update the q value
            q_value = ((1-self._learning_rate)*previous_q_value) + self._learning_rate * (reward + (self._discount_rate * next_state.get_max_value()))
            
            # set the new q value for the current state
            self._current_state.set_value(action,q_value)
            
            # update the current state
            self._current_state = next_state
            
            is_goal = False

        else:          
            # update the current state
            self._current_state = next_state

            is_goal = False
               
        
        return is_goal


    def get_action(self, state):
        # get coordinate of this state
        coordinates = self._state_space.get_coordinates(state)
        shape = self._state_space.get_shape()

        if random.uniform(0,1) > self._exploit_prob:
            # choose a random action
            action = state.get_random_action(coordinates,shape)
        else:
            # choose the best action
            action = state.get_best_action(coordinates,shape)

        return action

    # get the next state given an action
    def get_next_state(self,action, current_state):
        # get the coordinates of current state
        current_state_coordinates = self._state_space.get_coordinates(current_state)

        next_state_coordinates = (0,0)
        if action == Action.NORTH:
            next_state_coordinates = (current_state_coordinates[0]-1,current_state_coordinates[1])
        elif action == Action.SOUTH:
            next_state_coordinates = (current_state_coordinates[0]+1,current_state_coordinates[1])
        elif action == Action.EAST:
            next_state_coordinates = (current_state_coordinates[0],current_state_coordinates[1]+1)
        elif action == Action.WEST:
            next_state_coordinates = (current_state_coordinates[0],current_state_coordinates[1]-1)

        # get the state for this coordinates
        try:
            next_state = self._state_space.get_state(next_state_coordinates[0],next_state_coordinates[1])
        except Exception as e:
            print("{}:{}".format(current_state_coordinates,action.value))
            raise(e)

        return next_state

    def clamp_coordinates(self,coordinates, state_space):
        clamped_coordinates = (coordinates[0],coordinates[1])
        if coordinates[0] >= state_space.get_shape()[0]:
            clamped_coordinates = (coordinates[0]-1,coordinates[1])       
        elif coordinates[0] < 0:
            clamped_coordinates = (0,coordinates[1])

        if coordinates[1] >= state_space.get_shape()[1]:
            clamped_coordinates = (coordinates[0], coordinates[1]-1)       
        elif coordinates[1] < 0:
            clamped_coordinates = (coordinates[0], 0)
        return clamped_coordinates

    def get_optimal_policy(self,start_state):
        policy = []

        is_goal = False
        current_state = start_state
        while not is_goal:

            # get the best action for current state
            coordinates = self._state_space.get_coordinates(current_state)   
            action = current_state.get_best_action(coordinates,self._state_space.get_shape())
            state_action = (current_state, action)
            policy.append(state_action)

            # get the next state based on current state and action
            next_state = self.get_next_state(action,current_state)

            # check if is goal
            is_goal = next_state.get_type() == StateType.GOAL

            current_state = next_state

        return policy




