from __future__ import annotations

import random
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

import algorithms.evaluation as evaluation
from world.game import Agent, Directions

if TYPE_CHECKING:
    from world.game_state import GameState


class MultiAgentSearchAgent(Agent, ABC):
    """
    Base class for multi-agent search agents (Minimax, AlphaBeta, Expectimax).
    """

    def __init__(self, depth: str = "2", _index: int = 0, prob: str = "0.0") -> None:
        self.index = 0  # Drone is always agent 0
        self.depth = int(depth)
        self.prob = float(
            prob
        )  # Probability that each hunter acts randomly (0=greedy, 1=random)
        self.evaluation_function = evaluation.evaluation_function

    @abstractmethod
    def get_action(self, state: GameState) -> Directions | None:
        """
        Returns the best action for the drone from the current GameState.
        """
        pass


class RandomAgent(MultiAgentSearchAgent):
    """
    Agent that chooses a legal action uniformly at random.
    """

    def get_action(self, state: GameState) -> Directions | None:
        """
        Get a random legal action for the drone.
        """
        legal_actions = state.get_legal_actions(self.index)
        return random.choice(legal_actions) if legal_actions else None


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Minimax agent for the drone (MAX) vs hunters (MIN) game.
    """

    def get_action(self, state: GameState) -> Directions | None:
        """
        Returns the best action for the drone using minimax.

        Tips:
        - The game tree alternates: drone (MAX) -> hunter1 (MIN) -> hunter2 (MIN) -> ... -> drone (MAX) -> ...
        - Use self.depth to control the search depth. depth=1 means the drone moves once and each hunter moves once.
        - Use state.get_legal_actions(agent_index) to get legal actions for a specific agent.
        - Use state.generate_successor(agent_index, action) to get the successor state after an action.
        - Use state.is_win() and state.is_lose() to check terminal states.
        - Use state.get_num_agents() to get the total number of agents.
        - Use self.evaluation_function(state) to evaluate leaf/terminal states.
        - The next agent is (agent_index + 1) % num_agents. Depth decreases after all agents have moved (full ply).
        - Return the ACTION (not the value) that maximizes the minimax value for the drone.
    def minimax(state: GameState, agent_index: int) -> float:
        if state.is_win() or state.is_lose(): 
            return self.evaluation_function(state)
        
        agents= state.get_num_agents()
        acciones= state.get_legal_actions(agent_index)
        next_agent= (agent_index + 1) % agents
        
        if next_agent == 0: 
            return maxTurn(state, acciones, next_agent)
        else:
            return minTurn(state, acciones, next_agent)
        
    def maxTurn(state, acciones, agent_index) -> float:
        maximo= float('-inf')
        for a in acciones: 
            successor = state.generate_successor(agent_index, a)
            value = minimax(successor,next_agent)    
            maximo = max(value, maximo)
        
        return maximo
        
    def minTurn(state: GameState, acciones, agent_index) -> float:
        minimo= float('inf')
        for a in acciones: 
            successor = state.generate_successor(agent_index, a)
            value = minimax(successor,next_agent)    
            minimo = min(value, minimo)
        
        return minimo
        
    PROMPT: Eres un expero en algortimos de juegos de adversarios. Teniendo en cuenta los archivos en el workspace, 
    el codigo referencia proporcionado, y el problema tu tarea es corregir y complementar la funcion get_action en
    la clase minimax. Estoy teniendo problemas principalmente con el manejo de la profundidad  y las funciones, ya 
    que no estan correctamente definidas, pero me gustaria mantenerlas. Si es necesario utiliza contexto de game_state.py.
    Edita el archivo adversarial.py en la funcion indicada, y luego porporciona una lista de mejoras y cambios. 

    #Codigo referencia: [Codigo que esta arriba]
    #Problema (Este resumen fue realizado con IA): El problema plantea un escenario donde drones deben llevar suministros médicos a comunidades aisladas en la 
    selva amazónica, enfrentando tanto restricciones operacionales como amenazas externas. Se debe modelar la navegación del
    dron cuando aparecen cazadores adversarios. En este juego adversario, el dron es el agente MAX que busca entregar todos
    los suministros evitando ser capturado, mientras que los cazadores son agentes MIN que intentan interceptarlo moviéndose
    hacia su posición. El juego ocurre por turnos: el dron se mueve primero y luego cada cazador, y termina cuando el dron 
    completa todas las entregas (victoria) o cuando un cazador ocupa la misma casilla que el dron (derrota). El problema 
    se resuelve usando Minimax (y sus variantes) para decidir el mejor movimiento del dron anticipando las acciones de los 
    cazadores.
    
    
    
    Mejoras y cambios:
    1. Separé correctamente el retorno de get_action: ahora devuelve una Directions, 
    no un valor heurístico.
    2. Añadí una función recursiva interna minimax(...) para calcular utilidades numéricas
    sin romper la firma pública del agente.
    3. Corregí el manejo de profundidad: profundidad solo disminuye cuando termina un 
    ply completo, es decir, cuando el siguiente agente vuelve a ser el dron (next_agent == 0).
    4. Arreglé variables no definidas en el código original como agent_index y num_agents,
    usando self.index y state.get_num_agents().
    5. Hice que el dron sea nodo MAX y todos los cazadores nodos MIN, respetando el orden 
    de turnos del problema.
    6. Añadí casos base correctos para estados terminales, profundidad cero y 
    ausencia de acciones legales, evaluando con self.evaluation_function(state).
    7. Implementé la selección de la mejor acción en la raíz comparando 
    los valores minimax de cada sucesor.
    8. Eliminé el bloque inválido PROMPT: que dejaba la clase 
    en un estado inconsistente.
    9. Verifiqué sintaxis con python3 -m py_compile Drones/algorithms/adversarial.py.
        
        """
        def minimax(state: GameState, agent_index: int, profundidad: int) -> float:
            if state.is_win() or state.is_lose() or profundidad == 0:
                return self.evaluation_function(state)

            agents = state.get_num_agents()
            acciones = state.get_legal_actions(agent_index)

            if not acciones:
                return self.evaluation_function(state)

            next_agent = (agent_index + 1) % agents

            if agent_index == 0:
                return maxTurn(state, acciones, agent_index, next_agent, profundidad)
            return minTurn(state, acciones, agent_index, next_agent, profundidad)

        def maxTurn(
            state: GameState,
            acciones: list[Directions],
            agent_index: int,
            next_agent: int,
            profundidad: int,
        ) -> float:
            maximo = float("-inf")
            for a in acciones:
                successor = state.generate_successor(agent_index, a)
                siguiente_profundidad = profundidad - 1 if next_agent == 0 else profundidad
                value = minimax(successor, next_agent, siguiente_profundidad)
                maximo = max(value, maximo)

            return maximo

        def minTurn(
            state: GameState,
            acciones: list[Directions],
            agent_index: int,
            next_agent: int,
            profundidad: int,
        ) -> float:
            minimo = float("inf")
            for a in acciones:
                successor = state.generate_successor(agent_index, a)
                siguiente_profundidad = profundidad - 1 if next_agent == 0 else profundidad
                value = minimax(successor, next_agent, siguiente_profundidad)
                minimo = min(value, minimo)

            return minimo

        if state.is_win() or state.is_lose():
            return None

        acciones = state.get_legal_actions(self.index)
        if not acciones:
            return None

        mejor_accion = None
        maximo = float("-inf")
        agents= state.get_num_agents()

        for a in acciones:
            successor = state.generate_successor(self.index, a)
            next_agent = (self.index + 1) % agents
            profundidad = self.depth - 1 if next_agent == 0 else self.depth
            value = minimax(successor, next_agent, profundidad)

            if value > maximo:
                maximo = value
                mejor_accion = a

        return mejor_accion


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Alpha-Beta pruning agent. Same as Minimax but with alpha-beta pruning.
    MAX node: prune when value > beta (strict).
    MIN node: prune when value < alpha (strict).
    """

    def get_action(self, state: GameState) -> Directions | None:
        """
        Returns the best action for the drone using alpha-beta pruning.

        Tips:
        - Same structure as MinimaxAgent, but with alpha-beta pruning.
        - Alpha: best value MAX can guarantee (initially -inf).
        - Beta: best value MIN can guarantee (initially +inf).
        - MAX node: prune when value > beta (strict inequality, do NOT prune on equality).
        - MIN node: prune when value < alpha (strict inequality, do NOT prune on equality).
        - Update alpha at MAX nodes: alpha = max(alpha, value).
        - Update beta at MIN nodes: beta = min(beta, value).
        - Pass alpha and beta through the recursive calls.
        
        PROMPT: Segun el minimax propuesto esta el alphabeta completo y coherente? Pon las correcciones 
        en el codigo y agrega un comentario en las lineas adicionales
        """
        def alphabeta(state: GameState, agent_index: int, profundidad: int, alpha: float, beta: float) -> float:
            if state.is_win() or state.is_lose() or profundidad == 0:
                return self.evaluation_function(state)

            agents = state.get_num_agents()
            acciones = state.get_legal_actions(agent_index)

            if not acciones:
                return self.evaluation_function(state)

            next_agent = (agent_index + 1) % agents

            if agent_index == 0:
                return maxTurn(state, acciones, agent_index, next_agent, profundidad, alpha, beta)
            return minTurn(state, acciones, agent_index, next_agent, profundidad, alpha, beta)

        def maxTurn(
            state: GameState,
            acciones: list[Directions],
            agent_index: int,
            next_agent: int,
            profundidad: int,
            alpha: float,
            beta: float
        ) -> float:
            maximo = float("-inf")
            for a in acciones:
                successor = state.generate_successor(agent_index, a)
                siguiente_profundidad = profundidad - 1 if next_agent == 0 else profundidad
                value = alphabeta(successor, next_agent, siguiente_profundidad, alpha, beta)
                maximo = max(value, maximo)
                alpha = max(alpha, maximo)

                if maximo > beta:
                    break
                
            return maximo

        def minTurn(
            state: GameState,
            acciones: list[Directions],
            agent_index: int,
            next_agent: int,
            profundidad: int,
            alpha: float,
            beta: float
        ) -> float:
            minimo = float("inf")
            for a in acciones:
                successor = state.generate_successor(agent_index, a)
                siguiente_profundidad = profundidad - 1 if next_agent == 0 else profundidad
                value = alphabeta(successor, next_agent, siguiente_profundidad, alpha, beta)
                minimo = min(value, minimo)
                beta = min(beta, minimo)
                if minimo < alpha:
                    break  

            return minimo

        if state.is_win() or state.is_lose():
            return None

        acciones = state.get_legal_actions(self.index)
        if not acciones:
            return None

        mejor_accion = None
        maximo = float("-inf")
        agents = state.get_num_agents()
        alpha = float("-inf")  # Linea adicional: alpha inicial en la raiz
        beta = float("inf")  # Linea adicional: beta inicial en la raiz

        for a in acciones:
            successor = state.generate_successor(self.index, a)
            next_agent = (self.index + 1) % agents
            profundidad = self.depth - 1 if next_agent == 0 else self.depth
            value = alphabeta(
                successor, next_agent, profundidad, alpha, beta
            )  # Linea adicional: pasar alpha y beta a la recursion

            if value > maximo:
                maximo = value
                mejor_accion = a
            alpha = max(alpha, maximo)  # Linea adicional: actualizar alpha en la raiz

        return mejor_accion


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Expectimax agent with a mixed hunter model.

    Each hunter acts randomly with probability self.prob and greedily
    (worst-case / MIN) with probability 1 - self.prob.

    * When prob = 0:  behaves like Minimax (hunters always play optimally).
    * When prob = 1:  pure expectimax (hunters always play uniformly at random).
    * When 0 < prob < 1: weighted combination that correctly models the
      actual MixedHunterAgent used at game-play time.

    Chance node formula:
        value = (1 - p) * min(child_values) + p * mean(child_values)
    """

    def get_action(self, state: GameState) -> Directions | None:
        """
        Returns the best action for the drone using expectimax with mixed hunter model.

        Tips:
        - Drone nodes are MAX (same as Minimax).
        - Hunter nodes are CHANCE with mixed model: the hunter acts greedily with
          probability (1 - self.prob) and uniformly at random with probability self.prob.
        - Mixed expected value = (1-p) * min(child_values) + p * mean(child_values).
        - When p=0 this reduces to Minimax; when p=1 it is pure uniform expectimax.
        - Do NOT prune in expectimax (unlike alpha-beta).
        - self.prob is set via the constructor argument prob.
        """

        num_agents = state.get_num_agents()

        def expectimax(state, depth, agent_index):

            # estado terminal
            if state.is_win() or state.is_lose() or depth == 0:
                return self.evaluation_function(state)

            actions = state.get_legal_actions(agent_index)

            if not actions:
                return self.evaluation_function(state)

            next_agent = (agent_index + 1) % num_agents
            next_depth = depth - 1 if next_agent == 0 else depth

            # DRON (MAX)
            if agent_index == 0:
                value = float("-inf")
                for action in actions:
                    successor = state.generate_successor(agent_index, action)
                    value = max(value, expectimax(successor, next_depth, next_agent))
                return value

            # CAZADOR (CHANCE MIXTO)
            else:
                values = []
                for action in actions:
                    successor = state.generate_successor(agent_index, action)
                    values.append(expectimax(successor, next_depth, next_agent))

                p = self.prob

                greedy_value = min(values)
                mean_value = sum(values) / len(values)

                return (1 - p) * greedy_value + p * mean_value

        best_action = None
        best_value = float("-inf")

        for action in state.get_legal_actions(0):
            successor = state.generate_successor(0, action)
            value = expectimax(successor, self.depth, 1)

            if value > best_value:
                best_value = value
                best_action = action

        return best_action
