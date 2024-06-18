# bixie
Test Rubix cube solver


## TODO
- Add in using hashes to eliminate redundant analysis
- Add in a bidirectional search - instead of just searching from the start to the solution, start a tree from both ends and stop when you find an overlap
- Move get_heuristic() to CubeState class
- Introduce piece orientation
- Implement A* instead of whatever the fuck you have going right now
    This leads to a problem of having lots of repetitively checking for situations where the same face is moved twice in a row. Fix this one of two ways:
        - Only allow one clockwise turn at a time (but assign a cost of zero to turning the same face twice)
        - When a new node is created, automatically add the neighbours it shares with the parent node (the parent itself and five others)
    Experiment with both methods

    Also experiment with various different heuristics