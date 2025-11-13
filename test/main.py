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
          ["b/r" , "b/n" , "b/b" , "b/q" , "b/k" , "b/b" , "b/n" , "b/r"] ,
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

# pull up the possible moves of a piece
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
            if (x + src[0] <= 8 and y + src[1] <= 8 and x + src[0] >= -8 and y + src[1] >= -8) # -8<=x,y<=8
        ] # coords on board imagining there are no peices except the piece(in this case the rooooookkkkk).
        
        def 

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