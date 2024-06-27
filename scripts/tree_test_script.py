from scripts.cubeManipulation import *
from scripts.tree import *

myCube = CubeState()

from random import choice
for i in range(3):
    move = choice(possible_moves)
    print(move)
    myCube.turn( move )
    print(Node(myCube).get_heuristic())
    # randomise the cube (50 moves is more than enough, 20 is sufficient if there's no redundancy but there could be)

root = Node( myCube )
print(f"Starting heuristic: {root.get_heuristic()}")
print()

inferred_heuristics = [-99,-99,-99]
depth = 3
while True:
    root.analyse( depth )
    print()

    print(f"Preferred move: {root.preferred_child.move}")
    print(f"Inferred heuristic: {root.inferred_heuristic}")
    inferred_heuristics.append(root.inferred_heuristic)

    if root.inferred_heuristic <= min(inferred_heuristics[-2:]): # no progress being made
        print(f"No progress was made at depth {depth}, increasing depth by 1.")
        depth += 1
    else:
        depth = 3

    root = root.preferred_child.node # update to the new root
    print(f"Heuristic is now {root.get_heuristic()}")
    print()
    if root.get_heuristic() == 54: # fully solved cube
        break

print(len(hashes))
print(len(set(hashes)))