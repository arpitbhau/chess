# radhe radhe

import math

# board in a 2d array with row, col and board >>>>>> and ^^^^^^ in the array
board = [ ["w/r" , "w/n" , "w/b" , "w/q" , "w/k" , "w/b" , "w/n" , "w/r"] ,
          ["w/p" , "w/p" , "w/p" , "w/p" , "w/p" , "w/p" , "w/p" , "w/p"] ,
          ["___" , "___" , "___" , "___" , "___" , "___" , "___" , "___"] ,
          ["___" , "___" , "___" , "___" , "___" , "___" , "___" , "___"] ,
          ["___" , "___" , "___" , "___" , "___" , "___" , "___" , "___"] ,
          ["___" , "___" , "___" , "___" , "___" , "___" , "___" , "___"] ,
          ["b/p" , "b/p" , "b/p" , "b/p" , "b/p" , "b/p" , "b/p" , "b/p"] ,
          ["b/r" , "b/n" , "b/b" , "b/q" , "b/k" , "b/b" , "b/n" , "b/r"] 
]

# convert ACN to coords and vise versa
def coords_convert(val, arrF=False):
    """
        use arrF (arrayFormat) = True when u need coords for array indexing
    """
    
    # If input is a string like "d4"
    if isinstance(val, str):
        file_char = val[0].lower()
        rank_char = val[1]

        x = ord(file_char) - ord('a') + 1
        y = int(rank_char)

        # If arrF = True, subtract 1 from both (0-indexed)
        if arrF:
            x -= 1
            y -= 1

        return [x, y]

    # If input is a list or tuple like [x, y]
    if isinstance(val, (list, tuple)) and len(val) == 2:
        x, y = val

        # If the user gave 0-indexed coords, convert back to 1-indexed
        if arrF:
            x += 1
            y += 1

        file_char = chr(ord('a') + x - 1)
        rank_char = str(y)

        return f"{file_char}{rank_char}"

    raise ValueError("Invalid input")

# pulling up board data
def pull_board_square(sq):
    """
    takes the acn or coords[acc to board (1,1) is leftmost corner] and returns the position info as dict
    """

    # if array is given don't convert
    t = [sq[0] - 1 , sq[1] - 1] if sq is list else coords_convert(sq , arrF=True)

    return {
        "player": True if (board[t[0]][t[1]])[0] == "w" else False if (board[t[0]][t[1]])[0] == "b" else None,
        "piece": (board[t[0]][t[1]])[-1] ,
    }

# pull up the possible moves of a piece, src[1]
def pull_possible_moves(player , piece , src):
    """
        how the heck this works?
        => first consider the piece is at origin (0,0) and hardcode the coords possible for the specific piece,
        then shift the origin at src pt and you have the possible moves after that we filter the paths by manualy going thtough all the board squares.
    """

    moves = []
    src = coords_convert(src) # convert to coords from acn
    
    def rook_moves(player: bool):
        # acc to origin
        oCoords = [ [0,1] , [0,2] , [0,3] , [0,4] , [0,5] , [0,6] , [0,7] , # >>>
                    [1,0] , [2,0] , [3,0] , [4,0] , [5,0] , [6,0] , [7,0] , # ^^^
                    [-1,0] , [-2,0] , [-3,0] , [-4,0] , [-5,0] , [-6,0] , [-7,0] # <<<
                    [0,-1] , [0,-2] , [0,-3] , [0,-4] , [0,-5] , [0,-6] , [0,-7]  # down
                ]
        # shift the origin to src pt (only the coords which fit the board)
        shiftedCoords = [
            [x + src[0], y + src[1]]
            for x, y in oCoords
            if (x + src[0] <= 8 and y + src[1] <= 8 and x + src[0] >= 1 and y + src[1] >= 1) # 1<=x,y<=8
        ] # coords on board imagining there are no peices except the piece(in this case the rooooookkkkk).
        
        def filter_paths(coords , pt , direction):
            """coords: the list of coordinates to cycle
            pt: the refrence pt [x , y]
            coord:  the one coordinate which iterates in pt param."""
            # use path eqns for sorting. ** in this case x=a and y=b
            # for i in range(src[0] + t , 9): # (i , src[1]) --> coord to loop +x
            if not (pt[0] <= 8 and pt[0] >= 1 and pt[1] <= 8 and pt[1] >= 1 ):
                coords.remove(pt)
                return ""
            elif pt in coords:
                d = pull_board_square(pt).get("player")
                if d == player:
                    return ""
                elif d ==  (not player):
                    # moves.append(pt)
                    return f"{pt}"
                else:
                    coords.remove(pt)
                    new_pt = None
                    # new pt logic
                    match direction:
                        case "+x":
                            new_pt = [pt[0] + 1 , pt[1]]
                        case "-x":
                            new_pt = [pt[0] - 1 , pt[1]]
                        case "+y":
                            new_pt = [pt[0] , pt[1] + 1]
                        case "-y":
                            new_pt = [pt[0] , pt[1] - 1]
                        
                    return f"{pt} , {filter_paths(coords , pt=new_pt , direction=direction)}"
            else:
                coords.remove(pt) # remove that coord so that reecursion goes smoothly

        def finialize(coords):
            shifts = [
                (( 1,  0), "+x"),
                ((-1,  0), "-x"),
                (( 0,  1), "+y"),
                (( 0, -1), "-y"),
            ]

            all_moves = set()

            for (dx, dy), d_str in shifts:
                new_pt = [src[0] + dx, src[1] + dy]
                new_direction = d_str
                result = eval(filter_paths(coords, new_pt, new_direction))
                all_moves |= set(result)

            return list(all_moves)
        return finialize(shiftedCoords)
    
    return moves

# moving a piece 
def move(ACN):
    # destructure acn
    dACN = ACN.split(" ") # acn => "w r d2 d4"
    # move data
    mData = {
        "player": True if dACN[0] == "w" else False,
        "piece": dACN[1] ,
        "src": dACN[2] ,
        "dest": dACN[3]
    }
    # src and dest square data
    sData = pull_board_square(mData.get("src"))
    dData = pull_board_square(mData.get("dest"))

    # check the existence of src piece on board
    if sData.get("player") == mData.get("player") and sData.get("player") == mData.get("player"):
        pass