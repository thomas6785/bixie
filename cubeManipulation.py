import numpy as np

## Coordinate system:
# x,y,z
# positive x: blue
# negiatve x: green
# positive y: red
# negative y: orange
# positive z: white
# negative z: yellow

# 0,0,0 is the green, orange, yellow corner
# 2,2,2 is the blue, red, white corner
# 1,1,1 is the core

## storing colours
# the colours are stored as x,y,z
# for corner pieces this looks like [0,0,2]
# for edge pieces this looks like [0,1,2] (here y is the axis with no colour on this piece)
# this means a piece is in the correct position when its colour vector matches its coordinates

# create a 3x3x3 array of pieces
# create lookup tables of the coordinates of each ring piece on each face, going clockwise around the center
    # 6*2 lookup tables (2 per face, one of edges and one of corners)
    # in C/C++, these can be pointers instead of coordinate vectors (if I can wrap my head around the unbelievable level of pointer pointer pointers)
# use these lookup tables to rotate pieces around the 3x3x3 array of pieces
    # when doing so, also multiply orientation vector by a matrix dependent on the face being rotated (TODO figure out these matrices? they'll be a fourth root of the identity)

white_face_edges =    ( (0,1,2), (1,2,2), (2,1,2), (1,0,2) )   # z=2 counterclockwise when facing white
white_face_corners =  ( (0,0,2), (0,2,2), (2,2,2), (2,0,2) )   # z=2 counterclockwise when facing white
blue_face_edges =     ( (2,0,1), (2,1,2), (2,2,1), (2,1,0) )   # x=2 counterclockwise when facing blue
blue_face_corners =   ( (2,0,0), (2,0,2), (2,2,2), (2,2,0) )   # x=2 counterclockwise when facing blue
red_face_edges =      ( (1,2,0), (2,2,1), (1,2,2), (0,2,1) )   # y=2 counterclockwise when facing red
red_face_corners =    ( (2,2,0), (2,2,2), (0,2,2), (0,2,0) )   # y=2 counterclockwise when facing red

yellow_face_edges =   ( (1,0,0), (2,1,0), (1,2,0), (0,1,0) )   # z=0 counterclockwise when facing yellow
yellow_face_corners = ( (2,0,0), (2,2,0), (0,2,0), (0,0,0) )   # z=0 counterclockwise when facing yellow
green_face_edges =    ( (0,1,0), (0,2,1), (0,1,2), (0,0,1) )   # x=0 counterclockwise when facing green
green_face_corners =  ( (0,2,0), (0,2,2), (0,0,2), (0,0,0) )   # x=0 counterclockwise when facing green
orange_face_edges =   ( (0,0,1), (1,0,2), (2,0,1), (1,0,0) )   # y=0 counterclockwise when facing orange
orange_face_corners = ( (0,0,0), (0,0,2), (2,0,2), (2,0,0) )   # y=0 counterclockwise when facing orange

orientations = [ [ [ "N", "W", "Y" ], "R", "O" ], "B", "G" ]
# index this with orientations[x][y][z] to fetch the direction its facing from the vector

# This can just be a struct in C/C++, not a class
class Piece():
    def __init__(self, colours, orientation = [0,0,1]):
        self.orientation = orientation # default to 0,0,1 i.e. the imaginary white side if facing toward the white face, correct orientation
        self.colours = colours
        # colours[0] is 0 for green,  2 for blue,  1 for none
        # colours[1] is 0 for orange, 2 for red,   1 for none
        # colours[2] is 0 for yellow, 2 for white, 1 for none
        
        # self.type should be FACE, CORE, EDGE, or CORNER (just as a string for now, enum them in C)
        match self.colours.count(1):
            case 0: self.type = "CORNER"
            case 1: self.type = "EDGE"
            case 2: self.type = "FACE"
            case 3: self.type = "CORE"

class CubeState():
    def __init__(self, configuration=None):
        self.hash = None # only initialised when get_hash is called

        if configuration:
            self.pieces = configuration
        else:
            # If no configuration is specified, start in the solved state
            self.pieces = np.zeros((3,3,3),dtype=Piece)
            for x in range(3):
                for y in range(3):
                    for z in range(3):
                        self.pieces[x][y][z] = Piece( (x,y,z) )
    
    def output(self):
        for z in range(3):
            print(f"------------New z={z} layer-----------")
            for y in range(3):
                for x in range(3):
                    piece = self.pieces[x][y][z]
                    colours = [
                        ["GREEN (0)","NONE (1)","BLUE (2)"][piece.colours[0]],
                        ["ORANGE (0)","NONE (1)","RED (2)"][piece.colours[1]],
                        ["YELLOW (0)","NONE (1)","WHIE (2)"][piece.colours[2]]
                    ]
                    type = piece.type
                    match piece.orientation:
                        case [0,0,1]:  orientation = "WHITE"
                        case [0,0,-1]: orientation = "YELLOW"
                        case [0,1,0]:  orientation = "ORANGE"
                        case [0,-1,0]: orientation = "RED"
                        case [1,0,0]:  orientation = "BLUE"
                        case [-1,0,0]: orientation = "GREEN"
                    print((f"At {x},{y},{z}\t{type[:4]} piece {colours[0]}-{colours[1]}-{colours[2]}"+" "*50)[:50]+f" is facing toward {orientation}")

                print()

    def rotate_face_proto( self, face ): # rotates counterclockwise one turn (prototype)
        match face:
            case "WHITE":
                edges   = white_face_edges
                corners = white_face_corners
            case "BLUE":
                edges   = blue_face_edges
                corners = blue_face_corners
            case "RED":
                edges   = red_face_edges
                corners = red_face_corners
            case "YELLOW":
                edges   = yellow_face_edges
                corners = yellow_face_corners
            case "GREEN":
                edges   = green_face_edges
                corners = green_face_corners
            case "ORANGE":
                edges   = orange_face_edges
                corners = orange_face_corners

        # TODO implement orientation adjustments
        # TODO implement options for turning twice or reverse

        temp_piece = self.pieces[edges[3][0]][edges[3][1]][edges[3][2]]
        self.pieces[edges[3][0]][edges[3][1]][edges[3][2]] = self.pieces[edges[2][0]][edges[2][1]][edges[2][2]]
        self.pieces[edges[2][0]][edges[2][1]][edges[2][2]] = self.pieces[edges[1][0]][edges[1][1]][edges[1][2]]
        self.pieces[edges[1][0]][edges[1][1]][edges[1][2]] = self.pieces[edges[0][0]][edges[0][1]][edges[0][2]]
        self.pieces[edges[0][0]][edges[0][1]][edges[0][2]] = temp_piece

        temp_piece = self.pieces[corners[3][0]][corners[3][1]][corners[3][2]]
        self.pieces[corners[3][0]][corners[3][1]][corners[3][2]] = self.pieces[corners[2][0]][corners[2][1]][corners[2][2]]
        self.pieces[corners[2][0]][corners[2][1]][corners[2][2]] = self.pieces[corners[1][0]][corners[1][1]][corners[1][2]]
        self.pieces[corners[1][0]][corners[1][1]][corners[1][2]] = self.pieces[corners[0][0]][corners[0][1]][corners[0][2]]
        self.pieces[corners[0][0]][corners[0][1]][corners[0][2]] = temp_piece
    
    def turn( self, move ):
        face,turns = move
        # 'face' should be a string "WHITE", "BLUE", etc.
        # turns should be a number between 1 and 3
        # 1 for a single counterclockwise turn
        # 3 for a single clockwise turn
        
        # Currently this just calls the prototyped function three times
        # this is not efficient

        for i in range(turns):
            self.rotate_face_proto( face )
            # TODO make this way faster
            # currently it turns thrice to implement a backturn

    def get_hash( self ):
        if self.hash:
            return self.hash
        # need to store the position and orientation of all 20 mobile pieces
        
        hash = ["va:"]+["0000"]*39 # 'va' indicates the current hash 'version'. Not strictly necessary as it is constant, but may be useful if I store hashes externally and want to avoid mixing up versions. Change to vb next version
        i = 1
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    ortx,orty,ortz = self.pieces[x][y][z].orientation
                    hash[i] = (
                       "BxG"[self.pieces[x][y][z].colours[0]] # save the B/G colour
                     + "OxR"[self.pieces[x][y][z].colours[1]] # save the O/R colour
                     + "YxW"[self.pieces[x][y][z].colours[2]] # save the Y/W colour
                     + orientations[ortx][orty][ortz]         # save the orientation (WYBGOR)
                    )
                    i += 1
                hash[i] = " "
                i += 1
            hash[i] = "-- "
            i += 1
        
        return ''.join(hash[:-2])

        # TODO store the hash as a property not a function for speed
        # TODO compactify the hash to maximise use of each character (maybe use numbers instead of string)
        # TODO remove the core and face pieces, they're redundant