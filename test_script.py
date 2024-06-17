from cubeManipulation import *
from tree import *

myCube = CubeState()

from random import choice
for i in range(30):
    move = choice(possible_moves)
    myCube.turn( move )
    # randomise the cube (50 is more than enough, 20 is sufficient if there's no redundancy but there could be)

root = Node( myCube )
print(f"Starting heuristic: {root.get_heuristic()}")
print()

last_inferred_heuristic = -99 # placeholder
depth = 3
while True:
    root.analyse( depth )
    print()

    print(f"Preferred move: {root.preferred_child.move}")
    print(f"Inferred heuristic: {root.inferred_heuristic}")
    
    if root.inferred_heuristic <= last_inferred_heuristic: # no progress being made
        print(f"No progress was made at depth {depth}, increasing depth by 1.")
        depth += 1
    else:
        depth = 3
        last_inferred_heuristic = root.inferred_heuristic

        root = root.preferred_child.node # update to the new root
        print(f"Heuristic is now {root.get_heuristic()}")
        print()
        if root.get_heuristic() == 54: # fully solved cube
            break