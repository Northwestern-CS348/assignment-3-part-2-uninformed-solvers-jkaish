from student_code_game_masters import *
from student_code_uninformed_solvers import *
import time

th = TowerOfHanoiGame()
th.read('hanoi_5_all_disks_on_peg_one.txt')
required = [
    'fact: (movable disk1 peg3 peg1)',
    'fact: (movable disk1 peg3 peg2)',
]
th.setWinningCondition(required, 'hanoi_all_forbidden.txt')

solver = SolverBFS(th, ((), (), (1,2,3)))
s = th

# p8 = Puzzle8Game()
# p8.read('puzzle8_top_right_empty.txt')
# required = [
#     'fact: (movable tile6 pos3 pos2 pos3 pos3)',
#     'fact: (movable tile8 pos2 pos3 pos3 pos3)',
# ]
# p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')

# solver = SolverDFS(p8,((1,2,3),(4,5,6),(7,8,-1)))
# s = p8

num_steps = 0
start = time.time()
while not s.isWon():
    solver.solveOneStep()
    print('{}: {}'.format(num_steps, s.getGameState()))
    num_steps += 1

print(time.time() - start)
