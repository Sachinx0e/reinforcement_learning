from state_space import StateSpace
from agent import Agent
from state import StateType
import numpy as np
np.set_printoptions(edgeitems=30, linewidth=100000)

def main():
        
    # Paramaters
    epochs = 100
    learning_rate = 0.1
    discount_rate = 0.2
    exploit_prob = 0.1
    living_reward = -0.1
    
    # create a new state space
    state_space = StateSpace(4,4,
                            goal_1_position=(3,3),
                            goal_2_position=(3,2),
                            forbidden_position=(2,2),
                            wall_position=(2,3)
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
        
        print(iteration)
        iteration = iteration + 1
        

    # print state space
    print(state_space._space)

    # print the policy
    policy = agent.get_optimal_policy(start_state)
    flattened_state = state_space._space.flatten()
    for step in policy:
        state = step[0]
        index = np.where(flattened_state==state)[0]
        if state.get_type() == StateType.GOAL:
            print("{}: {}".format(index,"GOAL"))
        else:
            print("{}: {}".format(index,step[1].value))
 


if __name__ == "__main__":
    main()