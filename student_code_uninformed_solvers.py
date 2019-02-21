
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        curr_gs = self.currentState
        for m in self.gm.getMovables():
            self.gm.makeMove(m)
            gs = GameState(self.gm.getGameState(), self.currentState.depth + 1, m)
            gs.parent = curr_gs
            if gs not in self.visited.keys():
                self.visited[gs] = False
            self.currentState.children.append(gs)
            self.gm.reverseMove(m)

        found_next_step = False
        while not found_next_step and self.currentState.nextChildToVisit < len(self.currentState.children):
            next_state = self.currentState.children[self.currentState.nextChildToVisit]
            if self.visited[next_state]:
                self.currentState.nextChildToVisit += 1
            else:
                self.visited[next_state] = True
                self.currentState.nextChildToVisit += 1
                self.gm.makeMove(next_state.requiredMovable)
                self.currentState = next_state
                found_next_step = True

        # if not found_next_step:

        

        if self.currentState.state == self.victoryCondition:
            return True
        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        curr_gs = self.currentState
        for m in self.gm.getMovables():
            self.gm.makeMove(m)
            gs = GameState(self.gm.getGameState(), self.currentState.depth + 1, m)
            gs.parent = curr_gs
            if gs not in self.visited.keys():
                self.visited[gs] = False
            self.currentState.children.append(gs)
            self.gm.reverseMove(m)


        if self.currentState.state == self.victoryCondition:
            return True
        return False
