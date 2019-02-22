
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
        if not curr_gs.children:
            for m in self.gm.getMovables():
                # self.gm.makeMove(m)
                fut_gs = self.gm.createFutureGameState(curr_gs.state, m)
                gs = GameState(fut_gs, curr_gs.depth + 1, m)
                gs.parent = curr_gs
                if gs not in self.visited.keys():
                    self.visited[gs] = False
                curr_gs.children.append(gs)
                # self.gm.reverseMove(m)

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
        

        if self.currentState.state == self.victoryCondition:
            return True
        return False


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        return self.queue.pop(0)

    def peek(self):
        return self.queue[0]

    def empty(self):
        return len(self.queue) == 0


class SolverBFS(UninformedSolver):

    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = Queue()

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
            fut_gs = self.gm.createFutureGameState(curr_gs.state, m)
            gs = GameState(fut_gs, curr_gs.depth + 1, m)
            gs.parent = curr_gs
            if gs not in self.visited.keys():
                self.visited[gs] = False
            self.currentState.children.append(gs)
            self.queue.enqueue(gs)
            # self.gm.reverseMove(m)

        next_state = self.queue.dequeue()
        while self.visited[next_state]:
            next_state = self.queue.dequeue()

        temp = curr_gs
        while temp.requiredMovable:
            self.gm.reverseMove(temp.requiredMovable)
            temp = temp.parent

        temp = next_state.parent
        to_do = []
        while temp.requiredMovable:
            to_do.append(temp.requiredMovable)
            temp = temp.parent
        
        to_do.reverse()
        for td in to_do:
            self.gm.makeMove(td)


        self.gm.makeMove(next_state.requiredMovable)
        self.visited[next_state] = True
        self.currentState = next_state


        if self.currentState.state == self.victoryCondition:
            return True
        return False
