from operator import attrgetter

known_hashes = {}
possible_moves = [('WHITE', 1), ('WHITE', 2), ('WHITE', 3), ('YELLOW', 1), ('YELLOW', 2), ('YELLOW', 3), ('GREEN', 1), ('GREEN', 2), ('GREEN', 3), ('BLUE', 1), ('BLUE', 2), ('BLUE', 3), ('RED', 1), ('RED', 2), ('RED', 3), ('ORANGE', 1), ('ORANGE', 2), ('ORANGE', 3)]

import pickle
def copy(object):
    return pickle.loads(pickle.dumps(object))

class Node():
    def __init__( self, cubeState ):
        self.cubeState = cubeState
        self.neighbours = []
        self.neighbours_spawned = False
        self.heuristic = None

        # Used for A*
        self.came_from = None # Stores the best node to get here from
        self.came_from_move = None # Stores the last move for the best path to this node
        self.move_stack = [] # debugging purposes (for now?)
        self.gscore = None # Stores the cost of the cheapest path from start to n currently known (default infinity)
        self.fscore = None # Estimate of the path length from start to finish through this node - equal to gscore + heuristic (default infinity)
    
    def get_neighbours( self, known_close={} ):
        print("Extrapolating "+str(self.move_stack))
        if self.neighbours_spawned:
            return self.neighbours
        # known_close lets you pass in a hashtable of nodes known to be nearby to search before searching the main hashtable
        self.neighbours_spawned = True
        
        for move in possible_moves:
            newCubeState = copy( self.cubeState )
            newCubeState.turn( move )
            if newCubeState.get_hash() in known_close:
                self.neighbours.append(( move, known_close[newCubeState.get_hash()] ))
            elif newCubeState.get_hash() in known_hashes:
                self.neighbours.append(( move, known_hashes[newCubeState.get_hash()] ))
            else:
                new_neighbour = Node( newCubeState )
                known_hashes[ newCubeState.get_hash() ] = new_neighbour
                self.neighbours.append(( move, new_neighbour ))
        
        return self.neighbours

    def get_heuristic( self ):
        if self.heuristic:
            return self.heuristic
        
        # Simple heuristic: just add up how many PIECES are in the correct POSITION and the correct ORIENTATION
        self.heuristic = 54
        pieces = self.cubeState.pieces
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    if pieces[x][y][z].colours == (x,y,z):
                        self.heuristic -= 1
                        if pieces[x][y][z].orientation == [0,0,1]:
                            self.heuristic -= 1
        
        return self.heuristic
    
    def is_solved( self ):
        return self.get_heuristic() == 0 # todo remember to update this if the heuristic changes

def reconstruct_path( end_node ):
    total_path = [ end_node ]
    current_node = end_node
    moves = []
    while True:
        if current_node.came_from:
            total_path.insert(0,current_node.came_from)
            moves.insert(0,current_node.came_from_move)
            current_node = current_node.came_from
        else:
            return moves,total_path
    # TODO modify this to return a series of MOVES rather than nodes


def A_star( startNode ):
    frontier_nodes = [ startNode ]
    known_hashes[startNode.cubeState.get_hash()] = startNode

    startNode.gscore = 0 # by definition
    startNode.fscore = startNode.get_heuristic()

    while len(frontier_nodes) > 0:
        frontier_nodes = sorted(frontier_nodes, key=attrgetter('fscore'))
        current_node = frontier_nodes.pop(0)
        if current_node.is_solved():
            return reconstruct_path( current_node )
        
        for move,neighbour in current_node.get_neighbours():
            tentative_gscore = current_node.gscore + 1
            if not(neighbour.gscore) or tentative_gscore < neighbour.gscore:
                neighbour.came_from = current_node
                neighbour.came_from_move = move
                neighbour.move_stack = current_node.move_stack + [move]
                neighbour.gscore = tentative_gscore
                neighbour.fscore = tentative_gscore + neighbour.get_heuristic()
                if neighbour not in frontier_nodes:
                    frontier_nodes.append(neighbour)
    
    return None