from state_space import StateSpace
from agent import Agent

def test_step():
    # create an empty state space of 4,4
    state_space = StateSpace(4,4,
                             goal_1_position=(1,3),
                             goal_2_position=(3,3),
                             forbidden_position=(2,3),
                             wall_position=(2,2)
                             )

    # start state
    start_state = state_space.get_state(0,1)
    
    # create a new agent with this state space
    agent = Agent(state_space=state_space,
                    start_state=start_state,
                    learning_rate=0.1,
                    discount_rate=0.2,
                    exploit_prob=0.1,
                    living_reward=-0.1,
                    )
    # step
    assert agent.step() is not None