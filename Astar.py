class Node():
    def __init__( self, cubeState ):
        self.cubeState = cubeState
        self.neighbours = []
        self.neighbours_spawned = False
        self.heuristic = None

def A_star( startNode, heuristic ):
    frontier_nodes = [ startNode ]

    came_from = {}   # Stores the 'from' neighbour for each node
    gscore = {}      # Stores the cost of the cheapest path from start to n currently known
    gscore[ startNode ] = 0 # by definition
    # nodes with no entry in gscore should begin as infinite
    
    fscore = {} # fscore is the 'current best guess' of the cheapest path length from start to finish going through a given node (equal to gscore + heuristic at that node)
    # nodes with no entry in fscore should begin as infinite
    fscore[ startNode ] = startNode.get_heuristic()