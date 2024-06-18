# bixie
Test Rubix cube solver


## TODO
- Put 'ignorable moves' parameter in spawn_children() argument. When called, the moves passed in are ignored (e.g. the same face being moved twice, opposite faces being moved equivalently). If spawn children is called again on the same object, it will make sure all relevant children spawn
- Add in using hashes to eliminate redundant analysis
- Add in a bidirectional search - instead of just searching from the start to the solution, start a tree from both ends and stop when you find an overlap
- Move get_heuristic() to CubeState class

- Implement A* instead of whatever the fuck you have going right now
    This leads to a problem of having lots of repetitively checking for situations where the same face is moved twice in a row. Fix this one of two ways:
        - Only allow one clockwise turn at a time (put assign a cost of zero to turning the same face twice)
        - When a new node is created, automatically add the neighbours it shares with the parent node (the parent itself and five others)