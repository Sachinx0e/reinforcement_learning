from state_space import StateSpace
from action import Action
from state import StateType

def test_empty_by_default():
    # create an empty state space of 4,4
    state_space = StateSpace(4,4)

    # assert that state is not empty
    assert state_space.get_state(1,3) is not None

    # assert that q values for action are 0
    assert state_space.get_state(1,3).get_value(Action.NORTH) == 0
    assert state_space.get_state(1,3).get_value(Action.SOUTH) == 0
    assert state_space.get_state(1,3).get_value(Action.EAST) == 0
    assert state_space.get_state(1,3).get_value(Action.WEST) == 0


def test_initial_positions():
    # create an empty state space of 4,4
    state_space = StateSpace(4,4,
                             goal_1_position=(1,3),
                             goal_2_position=(3,3),
                             forbidden_position=(2,3),
                             wall_position=(2,2)
                             )

    # assert proper state types
    assert state_space.get_state(1,3).get_type() == StateType.GOAL
    assert state_space.get_state(3,3).get_type() == StateType.GOAL
    assert state_space.get_state(2,3).get_type() == StateType.FORBIDDEN
    assert state_space.get_state(2,2).get_type() == StateType.WALL


def test_get_coordinates():
    # create an empty state space of 4,4
    state_space = StateSpace(4,4,
                             goal_1_position=(1,3),
                             goal_2_position=(3,3),
                             forbidden_position=(2,3),
                             wall_position=(2,2)
                             )

    # assert proper state types
    goal_state = state_space.get_state(1,3)

    # assert that proper coordinates are returned
    goal_coordinates = state_space.get_coordinates(goal_state)
    assert goal_coordinates == (1,3)

    # assert that we get proper goal state on passing these coordinates back
    assert state_space.get_state(goal_coordinates[0], goal_coordinates[1]).get_type() == StateType.GOAL




