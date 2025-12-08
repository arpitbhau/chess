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
    t = [sq[1] - 1 , sq[0] - 1] if isinstance(sq , list) else coords_convert(sq , arrF=True)

    return {
        "player": True if (board[t[0]][t[1]])[0] == "w" else False if (board[t[0]][t[1]])[0] == "b" else None,
        "piece": (board[t[0]][t[1]])[-1] if not (board[t[0]][t[1]])[-1] == "_" else None,
    }

# find the peice
def find_piece(player , piece , output_format):
    """
    get the piece's location.
    player: True or False
    piece: r,n,b,q,k,p
    output_format=list or str
    return format [[1,2] , [2,2]] --> list or ["a2" , "b2"] --> str
    """    
    player = "w" if player else "b" # i'm a fucking genius!
    locations = []
    # x_coord, y_coord are in arrFromat make them to board by +1 into both of them.
    for y_coord,rank in enumerate(board): 
        for x_coord,r_sq in enumerate(rank): # r_sq means raw_sq in form of b/r
            if r_sq == f"{player}/{piece}":
                locations.append([x_coord+1, y_coord+1])
    return locations if output_format == list else [coords_convert(*coord) for coord in locations] # fucking insane!

# pinned peice logic
def get_pinned_peices(player):
    """
    returns the coords of piece and piece which are pinned for given player.[{piece:'r', coords:[2,2]} , {....}]
    sq: list or str type
    how the fuck this works?
    get all the attacking pieces of !player and draw a line from the !player's piece to the player's piece and check the slope of that line for respective piece,
    then check the availability of pts (sqaures) between the line's src and dest pts using the eqn of resective piece.
    """
    # pinned pieces
    pps = []
    
    # player's king's position
    p_king = find_piece(player=player, piece="k", output_format=list)[0]
    # path check between fns for rook and queen
    def rook_eq_check_between(r):
            """run check for both +x and -x the one which is not correct will drop out because of range() fn"""
            pinned = None # just declared something
            for idx, x in enumerate(range(p_king[0], r[0])): # rook is on right side of king
                if idx == 0: continue # skip king's square
                coord = [x , p_king[1]] # the y coord doesn't really matter here
                sq = pull_board_square(coord)
                if sq.get("player") == None:
                    continue
                elif sq.get("player") == player:
                    pinned = {"piece": sq.get("piece"), "coords": coord} if pinned == None else "they came with their gang"
                else: # sq = not player
                    break
            for idx, x in enumerate(range(r[0] , p_king[0])): # rook is in left side of king
                if idx == 0: continue # skip king's square
                coord = [x , p_king[1]] # the y coord doesn't really matter here
                sq = pull_board_square(coord)
                if sq.get("player") == None:
                    continue
                elif sq.get("player") == player:
                    pinned = {"piece": sq.get("piece"), "coords": coord} if pinned == None else "they came with their gang"
                else: # sq = not player
                    break
            for idx, y in enumerate(range(r[1] , p_king[1])): # rook is in up side of king
                if idx == 0: continue # skip king's square
                coord = [p_king[0], y] # the x coord doesn't really matter here
                sq = pull_board_square(coord)
                if sq.get("player") == None:
                    continue
                elif sq.get("player") == player:
                    pinned = {"piece": sq.get("piece"), "coords": coord} if pinned == None else "they came with their gang"
                else: # sq = not player
                    break
            for idx, y in enumerate(range(p_king[1], r[1])): # rook is on down side of king
                if idx == 0: continue # skip king's square
                print("ayo! it worked.")
                coord = [p_king[0], y] # the x coord doesn't really matter here
                sq = pull_board_square(coord)
                if sq.get("player") == None:
                    continue
                elif sq.get("player") == player:
                    pinned = {"piece": sq.get("piece"), "coords": coord} if pinned == None else "they came with their gang"
                else: # sq = not player
                    break
            
            pps.append(pinned)
    def bishop_eq_check_between(b):
            """run check for both +x and -x the one which is not correct will drop out because of range() fn"""
            pinned = None # just declared something
            for idx, x in enumerate(range(p_king[0] , b[0])): # bishop is in right side of king
                if idx == 0: continue # skip king's square
                coord = [x, p_king[1] + idx] if p_king[1] < b[1] else [x , p_king[1] - idx] # again im a fucking genius
                sq = pull_board_square(coord)
                if sq.get("player") == None:
                    continue
                elif sq.get("player") == player:
                    pinned = {"piece": sq.get("piece"), "coords": coord} if pinned == None else "they came with their gang"
                else: # sq = not player
                    break
            for idx, x in enumerate(range(b[0] , p_king[0])): # bishop is in left side of king
                if idx == 0: continue # skip king's square
                coord = [x, p_king[1] + 1] if p_king[1] < b[1] else [x , p_king[1] - 1] # again im a fucking genius
                sq = pull_board_square(coord)
                if sq.get("player") == None:
                    continue
                elif sq.get("player") == player:
                    pinned = {"piece": sq.get("piece"), "coords": coord} if pinned == None else "they came with their gang"
                else: # sq = not player
                    break
            pps.append(pinned) if not pinned == "they came with their gang" else None
    # get the attacking pieces of !player
    # 1. find all rooks of opponent and calc the pinned piece
    for r in find_piece(player=not player, piece="r", output_format=list):
        # draw line to !player's king and check slope of the line
        try:
            m = (r[1]-p_king[1]) / (r[0]-p_king[0])
            if m == 0: rook_eq_check_between(r=r) # m == 0, covers both 0deg and 180deg
        except ZeroDivisionError: # angle = 90deg or 270deg
            rook_eq_check_between(r=r)
    
    # 2. bishop ......
    for b in find_piece(player=not player, piece="b", output_format=list):
        # draw line to !player's king and check slope of the line
        m = (b[1]-p_king[1]) / (b[0]-p_king[0])
        if m in [-1 , 1]: bishop_eq_check_between(b=b)
    
    # 3. queen ......
    for q in find_piece(player=not player, piece="q", output_format=list):
        # draw line to !player's king and check slope of the line
        try:
            m = (q[1]-p_king[1]) / (q[0]-p_king[0])
            if m == 0: rook_eq_check_between(r=q) # rook
            elif m in [1, -1]: bishop_eq_check_between(b=q) # bishop
        except ZeroDivisionError:
            rook_eq_check_between(r=q) # rook with 90deg angle
    
    # future arpit here, i am too scared to touch my old code i fear that it might break when i try to change the data structure of returned value so im doing the filtering here after the dust has been settled.
    rook_pps, bishop_pps, queen_pps = [], [], []
    for pp in pps:
        match pp.get("piece"):
            case "r":
                rook_pps.append(pp.get("coords"))
            case "b":
                bishop_pps.append(pp.get("coords"))
            case "q":
                queen_pps.append(pp.get("coords"))

    return {"r": rook_pps, "b": bishop_pps, "q": queen_pps}

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
                    [-1,0] , [-2,0] , [-3,0] , [-4,0] , [-5,0] , [-6,0] , [-7,0], # <<<
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
    
    def bishop_moves(player: bool):
        # acc to origin
        oCoords = [ [1, 1] , [2,2] , [3 , 3] , [4,4] , [5,5] , [6,6] , [7,7] , # up right
                    [1,-1] , [2,-2] , [3,-3] , [4,-4] , [5,-5] , [6,-6] , [7,-7] , # down right
                    [-1,1] , [-2,2] , [-3,3] , [-4,4] , [-5,5] , [-6,6] , [-7,7] , # up left
                    [-1,-1] , [-2,-2] , [-3,-3] , [-4,-4] , [-5,-5] , [-6,-6] , [-7,-7]  # down left
                ]
        shiftedCoords = [
            [x + src[0], y + src[1]]
            for x, y in oCoords
            if (x + src[0] <= 8 and y + src[1] <= 8 and x + src[0] >= 1 and y + src[1] >= 1) # 1<=x,y<=8
        ] 
        
        def filter_paths(coords , pt , direction):
            """coords: the list of coordinates to cycle
            pt: the refrence pt [x , y]
            coord:  the one coordinate which iterates in pt param."""
            # use path eqns for sorting. ** in this case x=y
            if not (pt[0] <= 8 and pt[0] >= 1 and pt[1] <= 8 and pt[1] >= 1 ):
                return ""
            elif pt in coords:
                d = pull_board_square(pt).get("player")
                if d == player:
                    coords.remove(pt)
                    return ""
                elif d ==  (not player):
                    # moves.append(pt)
                    return f"{pt}"
                else:
                    coords.remove(pt)
                    new_pt = None
                    # new pt logic
                    match direction:
                        case "++":
                            new_pt = [pt[0] + 1 , pt[1] + 1]
                        case "+-":
                            new_pt = [pt[0] + 1 , pt[1] - 1]
                        case "--":
                            new_pt = [pt[0] - 1 , pt[1] - 1]
                        case "-+":
                            new_pt = [pt[0] - 1 , pt[1] + 1]
                        
                    return f"{pt} , {filter_paths(coords , pt=new_pt , direction=direction)}"
            else:
                coords.remove(pt) # remove that coord so that reecursion goes smoothly

        def finialize(coords):
            shifts = [
                (( 1,  1), "++"),
                ((-1, -1), "--"),
                (( 1, -1), "+-"),
                ((-1,  1), "-+"),
            ]

            all_moves = set()

            for (dx, dy), d_str in shifts:
                new_pt = [src[0] + dx, src[1] + dy]
                new_direction = d_str
                result = eval(filter_paths(coords, new_pt, new_direction))
                all_moves |= set(result)

            return list(all_moves)
        return finialize(shiftedCoords)

    def queen_moves(player: bool):
        return rook_moves(player) + bishop_moves(player)
    
    def knight_moves(player: bool):
        oCoords = [ [2,1] , [1,2] , [-1,2] , [-2,1] , [-2,-1] , [-1,-2] , [1,-2] , [2,-1] ]
        shiftedCoords = [
            [x + src[0], y + src[1]]
            for x, y in oCoords
            if (x + src[0] <= 8 and y + src[1] <= 8 and x + src[0] >= 1 and y + src[1] >= 1) # 1<=x,y<=8
        ] 
        valid_moves = []
        for pt in shiftedCoords:
            d = pull_board_square(pt).get("player")
            if d == player:
                continue
            elif d == (not player):
                valid_moves.append(pt)
            else:
                valid_moves.append(pt)
        return valid_moves

    def pawn_moves(player: bool):
        oCoords = [[-1,1] , [0,1] , [1,1]]
        shiftedCoords = [
            [x + src[0], y + src[1]]
            for x, y in oCoords
            if (x + src[0] <= 8 and y + src[1] <= 8 and x + src[0] >= 1 and y + src[1] >= 1) # 1<=x,y<=8
        ] 
        valid_moves = []
        for i, pt in enumerate(shiftedCoords):
            d = pull_board_square(pt).get("player")
            if i in [0 , 2] and d == (not player):
                valid_moves.append(pt) # TODO: en passant
            else:
                if d != None: valid_moves.append(pt)
        return valid_moves
    
    def king_moves(player: bool):
        oCoords = [[-1,1] , [0,1] , [1,1] , [1,0] , [1,-1] , [0,-1] , [-1,-1] , [-1,0]]
        shiftedCoords = [
            [x + src[0], y + src[1]]
            for x, y in oCoords
            if (x + src[0] <= 8 and y + src[1] <= 8 and x + src[0] >= 1 and y + src[1] >= 1) # 1<=x,y<=8
        ] 
        valid_moves = []
        for pt in shiftedCoords:
            d = pull_board_square(pt).get("player")
            if d == player:
                continue
            elif d == (not player):
                valid_moves.append(pt) # TODO: castling and much more
            else:
                valid_moves.append(pt)
        return valid_moves
    
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
    
print(get_pinned_peices(True))
