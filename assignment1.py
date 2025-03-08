from time import time
from search import *
from assignment1aux import *

def read_initial_state_from_file(filename):
    # Task 1
    # Return an initial state constructed using a configuration in a file.
    # Replace the line below with your code.

    # initialise state as a list of three elements
    # first element is the map
    # second element is the agent's location
    # third element is the agent's facing direction
    state = [None,None,None]
    with open(file="./assignment1config.txt", mode="r") as f:
        # the first two lines of the config file denote the rows and columns
        # of the zen garden
        rows = int(f.readline()[0])
        columns = int(f.readline()[0])

        # create map based on rows and columns
        # create this from a nested list comprehension
        map = [['' for _ in range(columns)] for _ in range(rows)]

        line = f.readline().strip()
        while line:
            values = line.split(',')
            rockRow = int(values[0])
            rockCol = int(values[1])
            map[rockRow][rockCol] = 'rock'
            line = f.readline()

    # map has been generated, so set to state's first element
    # tuple conversions: firstly the map then the state
    map = tuple(tuple(row) for row in map)
    state[0] = map
    state = tuple(state)

    return state

# ZenPuzzleGarden subclasses a Problem from the search.py library
class ZenPuzzleGarden(Problem):
    def __init__(self, initial):
        if type(initial) is str:
            super().__init__(read_initial_state_from_file(initial))
        else:
            super().__init__(initial)

    def actions(self, state):
        map = state[0]
        position = state[1]
        direction = state[2]
        height = len(map)
        width = len(map[0])
        action_list = []
        # if agent is on the map, specify ways which the agent can legally move
        if position:
            # if agent is facing up or down
            # given the agent is on the first column OR the space to its left is empty
            ## specify agent's current position and option to move left
            # given the agent is on the last column OR the space to its right is empty
            ## specify agent's current position and option to move right 
            if direction in ['up', 'down']:
                if position[1] == 0 or not map[position[0]][position[1] - 1]:
                    action_list.append((position, 'left'))
                if position[1] == width - 1 or not map[position[0]][position[1] + 1]:
                    action_list.append((position, 'right'))
            # if agent is facing left or right
            # given the agent is on the first row OR the space above is empty
            ## specify agent's current position and option to move up 
            # given the agent is on the last row OR the space below is empty
            ## specify agent's current position and option to move down
            if direction in ['left', 'right']:
                if position[0] == 0 or not map[position[0] - 1][position[1]]:
                    action_list.append((position, 'up'))
                if position[0] == height - 1 or not map[position[0] + 1][position[1]]:
                    action_list.append((position, 'down'))
        # if agent outside map, specify ways which the agent can enter:
        else:
            # iterate through each row, 
            # specify how to enter from the left edge
            # specify how to enter from the right edge
            for i in range(height):
                if not map[i][0]:
                    action_list.append(((i, 0), 'right'))
                if not map[i][width - 1]:
                    action_list.append(((i, width - 1), 'left'))
            # iterate through each column,
            # specify how to enter from the top edge
            # specify how to enter from the bottom edge
            for i in range(width):
                if not map[0][i]:
                    action_list.append(((0, i), 'down'))
                if not map[height - 1][i]:
                    action_list.append(((height - 1, i), 'up'))
        return action_list

    def result(self, state, action):
        map = [list(row) for row in state[0]]
        position = action[0]
        direction = action[1]
        height = len(map)
        width = len(map[0])
        while True:
            row_i = position[0]
            column_i = position[1]
            # guard clauses to specify agent's movement to new position based on direction
            # 5th guard clause analyses the new position:
            ## GIVEN the agent has exited from the top or bottom edge
            ## OR whether the agent has exited from the left edge or the right edge
            ## THEN modify the map to have the final direction
            ## AND return new map state, agent position and direction indicates exited problem space
            # 6th guard clause analyses the new position:
            ## GIVEN the agent has encountered a non empty position, i.e. a rock or raked tile
            ## THEN return new map state, agent position and direction indicates persistence in problem space
            # Otherwise agent has not exited, and has not encountered an obstacle:
            ## agent moves in the specified direction, position is retargeted, direction is perpetuated
            if direction == 'left':
                new_position = (row_i, column_i - 1)
            if direction == 'up':
                new_position = (row_i - 1, column_i)
            if direction == 'right':
                new_position = (row_i, column_i + 1)
            if direction == 'down':
                new_position = (row_i + 1, column_i)
            if new_position[0] < 0 or new_position[0] >= height or new_position[1] < 0 or new_position[1] >= width:
                map[row_i][column_i] = direction
                return tuple(tuple(row) for row in map), None, None
            if map[new_position[0]][new_position[1]]:
                return tuple(tuple(row) for row in map), position, direction
            map[row_i][column_i] = direction
            position = new_position

    def goal_test(self, state):
        # Task 2
        # Return a boolean value indicating if a given state is solved.
        # Replace the line below with your code.
        
        # goal test returns True when:
        ## all map cells are non empty
        ## agent position is None
        ## agent direction is None
        # otherwise goal test returns False
        solution = state[0]
        position = state[1]
        direction = state[2]
        for row in solution:
            for i in range(len(row)):
                if (not row[i]):
                    return False
        if (position == None and direction == None):
            return True
        else:
            return False 

# Task 3
# Implement an A* heuristic cost function and assign it to the variable below.
astar_heuristic_cost = None

def beam_search(problem, f, beam_width):
    # Task 4
    # Implement a beam-width version A* search.
    # Return a search node containing a solved state.
    # Experiment with the beam width in the test code to find a solution.
    # Replace the line below with your code.
    raise NotImplementedError

if __name__ == "__main__":

    # Task 1 test code
    
    print('The loaded initial state is visualised below.')
    visualise(read_initial_state_from_file('assignment1config.txt'))
    

    # Task 2 test code
    garden = ZenPuzzleGarden('assignment1config.txt')
    print('Running breadth-first graph search.')
    before_time = time()
    node = breadth_first_graph_search(garden)
    after_time = time()
    print(f'Breadth-first graph search took {after_time - before_time} seconds.')
    if node:
        print(f'Its solution with a cost of {node.path_cost} is animated below.')
        animate(node)
    else:
        print('No solution was found.')

    # Task 3 test code
    '''
    print('Running A* search.')
    before_time = time()
    node = astar_search(garden, astar_heuristic_cost)
    after_time = time()
    print(f'A* search took {after_time - before_time} seconds.')
    if node:
        print(f'Its solution with a cost of {node.path_cost} is animated below.')
        animate(node)
    else:
        print('No solution was found.')
    '''

    # Task 4 test code
    '''
    print('Running beam search.')
    before_time = time()
    node = beam_search(garden, lambda n: n.path_cost + astar_heuristic_cost(n), 50)
    after_time = time()
    print(f'Beam search took {after_time - before_time} seconds.')
    if node:
        print(f'Its solution with a cost of {node.path_cost} is animated below.')
        animate(node)
    else:
        print('No solution was found.')
    '''
