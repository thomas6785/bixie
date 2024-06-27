from Astar import *
from cubeManipulation import *

# Randomise a cube
myCube = CubeState()
from random import choice
for i in range(4):
    move = choice(possible_moves)
    print(move)
    myCube.turn( move )

root = Node( myCube )
print(f"Starting heuristic: {root.get_heuristic()}")
print()

sol = A_star( root )
print(sol)