import cv2
import numpy as np
from discretizer import Discretizer
from framework import MazeProblem, graph_search
import time
import os

def select_image():
    """Permite al usuario seleccionar una imagen de laberinto."""
    images = {
        "1": "Test.bmp",
        "2": "Test2.bmp",
        "3": "turing.bmp",
        "4": "Prueba Lab1.bmp"
    }
    
    print("\nSeleccione una imagen de laberinto:")
    for key, name in images.items():
        print(f"{key}. {name}")
    
    while True:
        choice = input("Ingrese el número de la opción: ").strip()
        if choice in images:
            return images[choice]
        print("Opción no válida. Intente nuevamente.")

def select_algorithm():
    """Permite al usuario seleccionar el algoritmo de búsqueda."""
    algorithms = {
        "1": ("bfs", "Breadth First Search"),
        "2": ("dfs", "Depth First Search"),
        "3": ("astar", "A* con heurística Manhattan"),
        "4": ("astar", "A* con heurística Euclidiana")
    }
    
    print("\nSeleccione el algoritmo de búsqueda:")
    for key, (_, name) in algorithms.items():
        print(f"{key}. {name}")
    
    while True:
        choice = input("Ingrese el número de la opción: ").strip()
        if choice in algorithms:
            algorithm = algorithms[choice]
            if choice == "4":
                return algorithm[0], "euclidean"
            return algorithm[0], "manhattan"
        print("Opción no válida. Intente nuevamente.")

def draw_solution(image, path, cell_size, algorithm_name):
    """Dibuja la solución en la imagen y añade información del algoritmo."""
    solution_image = image.copy()
    
    # Dibujar el camino
    for state in path:
        x, y = state.x * cell_size, state.y * cell_size
        cv2.rectangle(
            solution_image,
            (y, x),
            (y + cell_size, x + cell_size),
            (255, 0, 255),
            -1
        )
    
    # Añadir texto con información del algoritmo
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(
        solution_image,
        f"Algoritmo: {algorithm_name}",
        (10, 30),
        font,
        1,
        (0, 0, 255),
        2
    )
    
    return solution_image

def main():
    # Selección de imagen y algoritmo
    image_path = select_image()
    algorithm, heuristic = select_algorithm()
    
    # Configuración
    cell_size = 12
    discretizer = Discretizer(cell_size)
    
    print(f"\nLeyendo la imagen desde: {image_path}")
    print(f"Utilizando algoritmo: {algorithm}")
    if algorithm == "astar":
        print(f"Heurística: {heuristic}")
    
    # Procesamiento de la imagen
    try:
        maze_image = discretizer.read_image(image_path)
        discrete_maze = discretizer.discretize(maze_image)
        maze_problem = MazeProblem(discrete_maze)
        
        # Medir tiempo de ejecución
        start_time = time.time()
        solution = graph_search(maze_problem, algorithm, heuristic)
        end_time = time.time()
        
        if solution:
            path, actions = solution
            print(f"\nSolución encontrada en {end_time - start_time:.3f} segundos")
            print(f"Longitud del camino: {len(path)} pasos")
            
            # Mostrar pasos
            print("\nSecuencia de movimientos:")
            for i, (state, action) in enumerate(zip(path[1:], actions)):
                print(f"Paso {i + 1}: ({state.x}, {state.y}) - Moverse {action}")
            
            # Visualizar solución
            algorithm_name = {
                "bfs": "Breadth First Search",
                "dfs": "Depth First Search",
                "astar": f"A* ({heuristic})"
            }[algorithm]
            
            solution_image = draw_solution(maze_image, path, cell_size, algorithm_name)
            
            cv2.imshow("Solución del Laberinto", solution_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            # Guardar resultado en carpeta soluciones
            os.makedirs("soluciones", exist_ok=True)
            output_path = os.path.join("soluciones", f"solution_{algorithm}_{image_path.split('/')[-1]}")
            cv2.imwrite(output_path, solution_image)
            print(f"\nSolución guardada en: {output_path}")
        else:
            print("\nNo se encontró solución.")
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        return

main()