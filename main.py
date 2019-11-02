from state_space import StateSpace
from agent import Agent
from state import StateType
import numpy as np
np.set_printoptions(edgeitems=30, linewidth=100000)
from enum import Enum
import sys

def main(goal1_position, goal2_position, forbidden_position, wall_position, output_type, q_value_location):
        
    # Paramaters
    learning_rate = 0.1
    discount_rate = 0.2
    exploit_prob = 0.1
    living_reward = -0.1
    
    # create a new state space
    state_space = StateSpace(4,4,
                            goal_1_position=goal1_position,
                            goal_2_position=goal2_position,
                            forbidden_position=forbidden_position,
                            wall_position=wall_position
                            )

    # start state
    start_state = state_space.get_state(0,1)

    # create a new agent with this state space
    agent = Agent(state_space=state_space,
                      start_state=start_state,
                      learning_rate=learning_rate,
                      discount_rate=discount_rate,
                      exploit_prob=exploit_prob,
                      living_reward=living_reward
                      )

    # train
    
    # loop till we reach the convergence or complete the iterations
    iteration = 0
    has_converged = False
    while iteration <= 10000: 

        # get q values before making the step
        q_values_before_step = state_space.get_q_value_vector()
        
        # step
        agent.step()

        # q values after stepping
        q_values_after_step = state_space.get_q_value_vector()

        # check if values have converged
        has_converged = state_space.has_converged(q_values_before_step, q_values_after_step)
        
        if has_converged:
            break
        
        #print(iteration)
        iteration = iteration + 1
        

    # print state space
    #print(state_space._space)
    print("*********BOARD***********")
    state_space.render()

    # print the output
    if output_type == 'p':
        # get the policy
        print("*********POLICY***********")
        policy = state_space.get_policy()
        for key,value in policy.items():            
            print("{} {}".format(key,value))
    elif output_type == 'q':
        print("*********Q VALUES***********")
        # get the valus for state at the given position
        coordinate = StateSpace.to_coordinates(q_position)
        state = state_space.get_state(coordinate[0],coordinate[1])
        q_values = state.get_values()
        for action, value in q_values.items():
            print("{} {:.2f}".format(action.value,value))

if __name__ == "__main__":
    goal1_position = StateSpace.to_coordinates(int(sys.argv[1]))
    goal2_position = StateSpace.to_coordinates(int(sys.argv[2]))
    forbidden_position = StateSpace.to_coordinates(int(sys.argv[3]))
    wall_position = StateSpace.to_coordinates(int(sys.argv[4]))
    output_type = sys.argv[5]
    q_position = None
    if output_type == 'q':
        q_position = int(sys.argv[6])
    
    main(goal1_position,goal2_position,forbidden_position,wall_position,output_type,q_position)

    