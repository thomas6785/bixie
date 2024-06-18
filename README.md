# bixie
Test Rubix cube solver


## TODO
- Put 'ignorable moves' parameter in spawn_children() argument. When called, the moves passed in are ignored (e.g. the same face being moved twice, opposite faces being moved equivalently). If spawn children is called again on the same object, it will make sure all relevant children spawn
- Add in using hashes to eliminate redundant analysis
- Add in a bidirectional search - instead of just searching from the start to the solution, start a tree from both ends and stop when you find an overlap