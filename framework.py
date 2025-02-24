# framework.py
from abc import ABC, abstractmethod
from typing import List, Tuple, Set
import numpy as np
from dataclasses import dataclass
import heapq

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

class Node:
    """Nodo para el árbol de búsqueda."""
    def __init__(self, state, parent=None, action=None, path_cost=0, heuristic_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.heuristic_cost = heuristic_cost
        self.total_cost = path_cost + heuristic_cost
    
    def __lt__(self, other):
        return self.total_cost < other.total_cost

class Problem(ABC):
    @abstractmethod
    def initial_state(self) -> State:
        pass
    
    @abstractmethod
    def actions(self, state: State) -> List[str]:
        pass
    
    @abstractmethod
    def result(self, state: State, action: str) -> State:
        pass
    
    @abstractmethod
    def goal_test(self, state: State) -> bool:
        pass
    
    @abstractmethod
    def step_cost(self, state: State, action: str, next_state: State) -> float:
        pass
    
    @abstractmethod
    def heuristic(self, state: State, heuristic_type: str = "manhattan") -> float:
        pass

class MazeProblem(Problem):
    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix
        self.height, self.width = matrix.shape
        
        start_pos = np.where(matrix == 3)
        goal_positions = np.where(matrix == 2)
        
        if len(start_pos[0]) == 0 or len(goal_positions[0]) == 0:
            raise ValueError("El laberinto debe tener posiciones de inicio (3) y objetivo (2)")
            
        self.start_state = State(start_pos[0][0], start_pos[1][0])
        self.goal_positions = [State(x, y) for x, y in zip(goal_positions[0], goal_positions[1])]
        
        self.movements = {
            'up': (-1, 0),
            'right': (0, 1),
            'down': (1, 0),
            'left': (0, -1)
        }

    def initial_state(self) -> State:
        return self.start_state

    def actions(self, state: State) -> List[str]:
        valid_actions = []
        for action, (dx, dy) in self.movements.items():
            new_x = state.x + dx
            new_y = state.y + dy
            if (0 <= new_x < self.height and 
                0 <= new_y < self.width and 
                self.matrix[new_x, new_y] != 1):
                valid_actions.append(action)
        return valid_actions

    def result(self, state: State, action: str) -> State:
        if action not in self.movements:
            raise ValueError(f"Acción inválida: {action}")
        dx, dy = self.movements[action]
        return State(state.x + dx, state.y + dy)

    def goal_test(self, state: State) -> bool:
        return state in self.goal_positions

    def step_cost(self, state: State, action: str, next_state: State) -> float:
        return 1.0

    def heuristic(self, state: State, heuristic_type: str = "manhattan") -> float:
        if heuristic_type == "manhattan":
            # Distancia Manhattan al objetivo más cercano
            return min(abs(state.x - goal.x) + abs(state.y - goal.y) 
                      for goal in self.goal_positions)
        elif heuristic_type == "euclidean":
            # Distancia Euclidiana al objetivo más cercano
            return min(((state.x - goal.x) ** 2 + (state.y - goal.y) ** 2) ** 0.5 
                      for goal in self.goal_positions)
        else:
            raise ValueError(f"Tipo de heurística no válido: {heuristic_type}")

def graph_search(problem: Problem, strategy: str, heuristic_type: str = "manhattan"):
    """Implementación genérica de búsqueda en grafos."""
    
    if strategy == "bfs":
        return breadth_first_search(problem)
    elif strategy == "dfs":
        return depth_first_search(problem)
    elif strategy == "astar":
        return astar_search(problem, heuristic_type)
    else:
        raise ValueError(f"Estrategia de búsqueda no válida: {strategy}")

def breadth_first_search(problem: Problem):
    """Implementación de BFS."""
    from collections import deque
    
    node = Node(problem.initial_state())
    if problem.goal_test(node.state):
        return reconstruct_path(node)
    
    frontier = deque([node])
    explored = set()
    
    while frontier:
        node = frontier.popleft()
        explored.add(node.state)
        
        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            child_node = Node(
                child_state,
                parent=node,
                action=action,
                path_cost=node.path_cost + problem.step_cost(node.state, action, child_state)
            )
            
            if child_state not in explored and not any(n.state == child_state for n in frontier):
                if problem.goal_test(child_state):
                    return reconstruct_path(child_node)
                frontier.append(child_node)
    
    return None

def depth_first_search(problem: Problem):
    """Implementación de DFS."""
    node = Node(problem.initial_state())
    if problem.goal_test(node.state):
        return reconstruct_path(node)
    
    frontier = [node]
    explored = set()
    
    while frontier:
        node = frontier.pop()
        explored.add(node.state)
        
        for action in reversed(problem.actions(node.state)):
            child_state = problem.result(node.state, action)
            child_node = Node(
                child_state,
                parent=node,
                action=action,
                path_cost=node.path_cost + problem.step_cost(node.state, action, child_state)
            )
            
            if child_state not in explored and not any(n.state == child_state for n in frontier):
                if problem.goal_test(child_state):
                    return reconstruct_path(child_node)
                frontier.append(child_node)
    
    return None

def astar_search(problem: Problem, heuristic_type: str = "manhattan"):
    """Implementación de A* con heurística seleccionable."""
    node = Node(
        problem.initial_state(),
        heuristic_cost=problem.heuristic(problem.initial_state(), heuristic_type)
    )
    
    if problem.goal_test(node.state):
        return reconstruct_path(node)
    
    frontier = []
    heapq.heappush(frontier, node)
    explored = set()
    frontier_states = {node.state}
    
    while frontier:
        node = heapq.heappop(frontier)
        frontier_states.remove(node.state)
        
        if problem.goal_test(node.state):
            return reconstruct_path(node)
        
        explored.add(node.state)
        
        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            
            if child_state in explored:
                continue
                
            child_cost = node.path_cost + problem.step_cost(node.state, action, child_state)
            child_node = Node(
                child_state,
                parent=node,
                action=action,
                path_cost=child_cost,
                heuristic_cost=problem.heuristic(child_state, heuristic_type)
            )
            
            if child_state not in frontier_states:
                heapq.heappush(frontier, child_node)
                frontier_states.add(child_state)
    
    return None

def reconstruct_path(node: Node):
    """Reconstruye el camino desde el nodo inicial hasta el nodo objetivo."""
    path = []
    actions = []
    
    while node:
        path.append(node.state)
        actions.append(node.action)
        node = node.parent
    
    path.reverse()
    actions.reverse()
    actions.pop(0)  # Remove None action from start state
    
    return path, actions