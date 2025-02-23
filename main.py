import cv2
import numpy as np
from discretizer import Discretizer
from framework import MazeProblem, State

def breadth_first_search(problem):
    from collections import deque

    frontier = deque([problem.initial_state()])
    explored = set()
    parent_map = {problem.initial_state(): None}

    while frontier:
        state = frontier.popleft()
        if problem.goal_test(state):
            return reconstruct_path(parent_map, state)

        explored.add(state)
        for action in problem.actions(state):
            child = problem.result(state, action)
            if child not in explored and child not in frontier:
                parent_map[child] = state
                frontier.append(child)

    return None

def reconstruct_path(parent_map, state):
    path = []
    while state is not None:
        path.append(state)
        state = parent_map[state]
    path.reverse()
    return path

def main():
    image_path = "Test2.bmp"
    cell_size = 12

    discretizer = Discretizer(cell_size)
    maze_image = discretizer.read_image(image_path)
    discrete_maze = discretizer.discretize(maze_image)

    maze_problem = MazeProblem(discrete_maze)
    solution_path = breadth_first_search(maze_problem)

    if solution_path:
        print("Solución encontrada:")
        for state in solution_path:
            print(f"({state.x}, {state.y})")
    else:
        print("No se encontró solución.")

if __name__ == "__main__":
    main()