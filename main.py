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

def draw_solution(image, path, cell_size):
    for state in path:
        x, y = state.x * cell_size, state.y * cell_size
        cv2.rectangle(image, (y, x), (y + cell_size, x + cell_size), (255, 0, 255), -1) 
    return image

def main():
    image_path = input("Por favor, ingrese la ruta de la imagen (Ej : Test2.bmp): ")
    cell_size = 12

    discretizer = Discretizer(cell_size)
    print(f"Leyendo la imagen desde: {image_path}")
    discretizer = Discretizer(cell_size=12)

    maze_image = discretizer.read_image(image_path)

    discrete_maze = discretizer.discretize(maze_image)

    for row in discrete_maze:
        print(" ".join(map(str, row)))

    maze_problem = MazeProblem(discrete_maze)
    solution_path = breadth_first_search(maze_problem)

    if solution_path:
        print("Solución encontrada:")
        for index, state in enumerate(solution_path):
            if index == 0:
                print(f"Paso {index + 1}: ({state.x}, {state.y}) - Inicio")
            else:
                prev_state = solution_path[index - 1]
                if state.x < prev_state.x:
                    move = "arriba"
                elif state.x > prev_state.x:
                    move = "abajo"
                elif state.y < prev_state.y:
                    move = "izquierda"
                elif state.y > prev_state.y:
                    move = "derecha"
                print(f"Paso {index + 1}: ({state.x}, {state.y}) - Moverse {move}")

        # Dibujar la solución
        solution_image = draw_solution(maze_image, solution_path, cell_size)
        cv2.imshow("Solución del Laberinto", solution_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No se encontró solución.")


main()