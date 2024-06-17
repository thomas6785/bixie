from operator import attrgetter

possible_moves = [('WHITE', 1), ('WHITE', 2), ('WHITE', 3), ('YELLOW', 1), ('YELLOW', 2), ('YELLOW', 3), ('GREEN', 1), ('GREEN', 2), ('GREEN', 3), ('BLUE', 1), ('BLUE', 2), ('BLUE', 3), ('RED', 1), ('RED', 2), ('RED', 3), ('ORANGE', 1), ('ORANGE', 2), ('ORANGE', 3)]

import pickle
def copy(object):
    return pickle.loads(pickle.dumps(object))

# struct
class Child_Link():
    def __init__(self, oldCubeState, move ):
        newCubeState = copy(oldCubeState)
        newCubeState.turn( move )

        self.node = Node( newCubeState )
        self.move = move

        # add hashing to avoid duplicates here TODO

class Node():
    def __init__( self, cubeState ):
        self.cubeState = cubeState
        self.heuristic = None # only initialised when get_heuristic is called
        self.inferred_heuristic = None

        self.children = []
        self.has_children = False

        # okay so hashing to avoid duplicates is fine
        # not moving the same face twice is fine
        # and not moving opposing faces if the dominant face was last turned is fine
        # that reduces branching factor to 13.5
        # but using all three at the same time might not be fine
        # gets tricky
    
    def spawn_children( self ):
        for move in possible_moves:
            self.children.append( Child_Link( self.cubeState, move ) )
        self.has_children = True

    def analyse( self, depth ):
        # TODO implement alpha-beta pruning
        if not(self.has_children):
            self.spawn_children()
        
        if self.get_heuristic() == 54:
            self.inferred_heuristic = self.get_heuristic() + depth # add the current depth to give a bonus for using less moves
            self.analysed_depth = depth
            # hacky, todo fix that
        
        elif depth == 0:
            self.inferred_heuristic = self.get_heuristic()
            self.analysed_depth = 0
        
        else:
            if depth > 1: print(depth,end=" ")
            for child in self.children:
                child.node.analyse(depth-1)
            
            self.preferred_child = sorted(self.children,key=attrgetter('node.inferred_heuristic'))[-1] # get the best child
            self.inferred_heuristic = self.preferred_child.node.inferred_heuristic # update inferred heuristic and increase the inference depth
            self.analysed_depth = depth
            self.preferred_move = self.preferred_child.move # and our preferred move
        
    
    def get_heuristic( self ):
        if self.heuristic:
            return self.heuristic
        
        # Simple heuristic: just add up how many PIECES are in the correct POSITION and the correct ORIENTATION
        self.heuristic = 0
        pieces = self.cubeState.pieces
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    if pieces[x][y][z].colours == (x,y,z): self.heuristic += 1
                    if pieces[x][y][z].orientation == [0,0,1]: self.heuristic += 1
        
        return self.heuristic