Possible to identify 'clusters' of 16 states which are related by movements strictly along one axis
e.g. by only touching the white and yellow faces, you can access 16 states, all within one or two movements.

Each state is in three such clusters (one for each axis), therefore cluster has 32 clusters with which it shares a state

Every node in a given cluster has each 'layer' along the cluster's axis constant. i.e. for an white-yellow-axis cluster, the:
    - white face remains the same *relative to itself* (it may rotate)
    - yellow face remains the same *relative to itself* (it may rotate too)
    - center slice remains the same
We can therefore easily identify which cluster a state belongs to

So we can spot the 'solved' cluster easily
and create a lookup table of neighbouring clusters to the solved cluster
    1
    32 (within one cluster jump)
        Each of those 32 links to:
            The original
            Another of the 32
            30 others
            Therefore at twp cluster jumps there are
    960 (within two cluster jumps)

    So by just storing 993 clusters, we can know every state within four moves of the solved state

Say you are in cluster A and wish to move to cluster B
Cluster A has 16 states:
    - one of them is shared with cluster B (you are already in cluster B)
    - six of them are one move from cluster B
    - nine of them are two moves from cluster B
On average, if you are in Cluster A and NOT in Cluster B, moving to Cluster B will take 6/15 + 2*9/15 = 1.6 moves

Because each node is a member of three clusters, clusters appear in triangles (ie. if state A is in cluster 1, 2, and 3, all three are connected)
Each triangle on the cluster map corresponds to a state
Each state draws a triangle of three clusters on the cluster map
    So we have 16 triangles per cluster (total 43 quintillion triangles)

So what if we view each group of three clusters as a 'supercluster'?
    Well, now each 'supercluster' represents 48 positions
    Each cluster is a member of 16 superclusters
    A supercluster is basically just the set of states reachable from some core state by moving on any ONE axis
    Okay that's not a very useful insight unless I can identify some property every state in the supercluster has in common

Remember each cluster has an x, y, or z 'colouring' and you must change colouring each time

(From a computational standpoint, it may be simplest to pick a 'canonical' state from each cluster, and consider the distance to neighbouring clusters as the distance between canonical states (either one or two moves))
(Mathematically, a 'cluster jump' is not an exact number of moves, it may be one or two, averaging 1.6)
(If we minimise 'cluster jumps' we are not NECESSARILY minimising the total moves, but it can't be a bad thing)

There are 2.7e18 clusters






What about clusters beyond just one axis
What about all the positions reachable by manipulating only two perpendicular faces?
    Do a simulation to find all of them
    Notice that they have a lot in common - 7/20 cube pieces are untouchable in this arrangement
    Having those 7 pieces in common does not necessarily mean two pieces are in the same cluster of this kind, but its a good clue

    Question: consider all the cubes which share the 7 mobile pieces not touching the white and green faces -c call this set X. Now consider you can only move the white and green faces. How many subsets of X are there which you cannot move between? How large are they?

Extend this idea: what if we are only allowed to manipulate three perpendicular faces? There are now just four untouchable pieces

What if we could move white, yellow, and green? How many states are accessible?






Another different idea: rings
Consider an arbitrary manoeuvre - for example, White_1-Green_1. Repeating this enough will ALWAYS return to the original state - but how many turns will it take?
Defining any manoeuvre creates a set of 'rings' in the node space, which you cannot move between

The simple manoeuvre white_1 (or similar) has a ring length of 4
The manoeuvre white_1-green_1 has a ring length of 37 (I think?)

If we could identify a common characteristic for certain rings, then we could identify easily which ring sets we are a part of
From there, we could identiy how to move between them through various manoeuvres.


Thinking more about rings, being able to identify invariants in a ring could be extremely useful
If we can spot an invariant in a given ring, we can know that two positions are related by that ring's manoeuvre just by them sharing that invariant!
