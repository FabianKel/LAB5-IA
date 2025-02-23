from abc import ABC, abstractmethod
from typing import List, Tuple, Set
import numpy as np
from dataclasses import dataclass

@dataclass
class State:
    """Representa un estado en el problema del laberinto."""
    x: int
    y: int

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

class Problem(ABC):
    ##Clase base abstracta para el marco del problema
    
    @abstractmethod
    def initial_state(self) -> State:
        ##Devuelve el estado inicial del problema
        pass
    
    @abstractmethod
    def actions(self, state: State) -> List[str]:
        ##Devuelve lista de acciones válidas desde un estado dado.
        pass
    
    @abstractmethod
    def result(self, state: State, action: str) -> State:
        ##Devuelve el estado que resulta de tomar una acción en un estado
        pass
    
    @abstractmethod
    def goal_test(self, state: State) -> bool:
        ##Devuelve True si el estado es un estado objetivo
        pass
    
    @abstractmethod
    def step_cost(self, state: State, action: str, next_state: State) -> float:
        ##Devuelve el costo de tomar una acción desde un estado al siguiente
        pass

class MazeProblem(Problem):
    ##Implementación del marco del problema para navegación en laberinto
    
    def __init__(self, matrix: np.ndarray):
        """
        Inicializa el problema del laberinto con una matriz discretizada.
        0: camino (blanco)
        1: pared (negro)
        2: objetivo (verde)
        3: inicio (rojo)
        """
        self.matrix = matrix
        self.height, self.width = matrix.shape
        
        # Encontrar posiciones de inicio y objetivo
        start_pos = np.where(matrix == 3)
        goal_pos = np.where(matrix == 2)
        
        if len(start_pos[0]) == 0 or len(goal_pos[0]) == 0:
            raise ValueError("El laberinto debe tener posiciones de inicio (3) y objetivo (2)")
            
        self.start_state = State(start_pos[0][0], start_pos[1][0])
        self.goal_state = State(goal_pos[0][0], goal_pos[1][0])
        
        # Definir movimientos posibles: arriba, derecha, abajo, izquierda
        self.movements = {
            'up': (-1, 0),     # arriba
            'right': (0, 1),   # derecha
            'down': (1, 0),    # abajo
            'left': (0, -1)    # izquierda
        }

    def initial_state(self) -> State:
        return self.start_state

    def actions(self, state: State) -> List[str]:
        ##Devuelve lista de movimientos válidos desde el estado actual
        valid_actions = []
        
        for action, (dx, dy) in self.movements.items():
            new_x = state.x + dx
            new_y = state.y + dy
            
            # Verificar si el movimiento está dentro de los límites y no hacia una pared
            if (0 <= new_x < self.height and 
                0 <= new_y < self.width and 
                self.matrix[new_x, new_y] != 1):
                valid_actions.append(action)
                
        return valid_actions

    def result(self, state: State, action: str) -> State:
        ##Devuelve nuevo estado después de realizar una acción.
        if action not in self.movements:
            raise ValueError(f"Acción inválida: {action}")
            
        dx, dy = self.movements[action]
        new_x = state.x + dx
        new_y = state.y + dy
        
        # Validar nueva posición
        if not (0 <= new_x < self.height and 0 <= new_y < self.width):
            raise ValueError("La acción lleva fuera de los límites del laberinto")
            
        if self.matrix[new_x, new_y] == 1:
            raise ValueError("La acción lleva hacia una pared")
            
        return State(new_x, new_y)

    def goal_test(self, state: State) -> bool:
        ##Verifica si el estado actual es el estado objetivo
        return state == self.goal_state

    def step_cost(self, state: State, action: str, next_state: State) -> float:
        ##Devuelve el costo de la acción
        return 1.0

    def get_neighbors(self, state: State) -> Set[State]:
        ##Método auxiliar para obtener todos los estados vecinos
        neighbors = set()
        for action in self.actions(state):
            neighbors.add(self.result(state, action))
        return neighbors