# radhe radhe

# fucking bandage for the wound named init fn
# board is in diretcion --> = +x on board and down = +y on board 
board = [
        ["w/r" , "w/n" , "w/b" , "w/q" , "w/k" , "w/b" , "w/n" , "w/r"] ,
        ["w/p" , "w/p" , "w/p" , "w/p" , "w/p" , "w/p" , "w/p" , "w/p"] ,
        ["___" , "___" , "___" , "___" , "___" , "___" , "___" , "___"] ,
        ["___" , "___" , "___" , "___" , "___" , "___" , "___" , "___"] ,
        ["___" , "___" , "___" , "___" , "___" , "___" , "___" , "___"] ,
        ["___" , "___" , "___" , "___" , "___" , "___" , "___" , "___"] ,
        ["b/p" , "b/p" , "b/p" , "b/p" , "b/p" , "b/p" , "b/p" , "b/p"] ,
        ["b/r" , "b/n" , "b/b" , "b/q" , "b/k" , "b/b" , "b/n" , "b/r"] 
]
board_copy = board.copy()
en_passant=None
check=None
castleRights={"w": True, "b": True}
game_status=None
moves_sheet = open(f"./moves_sheet.txt", "a")

# convert ACN to coords and vise versa
def coords_convert(val: str | list, arrF=False):
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
def pull_board_square(sq: str | list):
    """
    takes the acn or coords[acc to board (1,1) is leftmost corner] and returns the position info as dict
    """

    # if array is given don't convert
    t = [sq[1] - 1 , sq[0] - 1] if isinstance(sq , list) else coords_convert(sq , arrF=True)

    return {
        "player": True if (board[t[0]][t[1]])[0] == "w" else False if (board[t[0]][t[1]])[0] == "b" else None,
        "piece": (board[t[0]][t[1]])[-1] if not (board[t[0]][t[1]])[-1] == "_" else None,
    }

# place piece onto board
def place_piece(player: bool, piece: str, src: list, dest: list):
    # change board
    board[src[1] - 1][src[0] - 1] = "___"
    board[dest[1] - 1][dest[0] - 1] = f"{'w' if player else 'b'}/{piece}"
    return 200

# find the peice
def find_piece(player:bool, piece:str, output_format: type):
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
                locations.append([x_coord+1, y_coord+1]) # +1 because the coords were accordig to array indexing i.e 0,0 is origin 
    return locations if output_format == list else [coords_convert(*coord) for coord in locations] # fucking insane!

# get protectors of a piece
def get_protectors(protector: bool, cos: list): # really, cos? come on dude - by_myself
    """ give 'coords of square(cos)' of whose protectors are to be found and the guy who u want to see protecting(i mean white or black, mochiron True or False).
    returns {'player': player, 'pieces': [{'piece': 'example_piece', coords: [example_coords]}, ....]}
    if no pieces returns 'None'
    """
    # logic: kinda similiar algo to pinned piece algo
    victim = cos # just renamed to a better name

    # future arpit here, i used both cos and victim in the code. idk i was not drunk when i wrote this fn but i just messed this up and now i dont wanna touch this shitty code again. i m leaving this as a mark of how dumb i can get sometimes.

    rook_protectors=[]
    knight_protectors=[]
    bishop_protectors=[]
    queen_protectors=[]
    king_protectors=[]
    pawn_protectors=[]

    # find victim's allies
    # 1. THE ROOOOOKKKKK!!!!
    def rook_eq_check_between(r: list, queen_bandage_to_fn=False):
        """run check for both +x and -x the one which is not correct will drop out because of range() fn"""
        protecting_guy = None # just declared something
        for idx, x in enumerate(range(victim[0], r[0])): # rook is on right side of king
            coord = [x , victim[1]] # the y coord doesn't really matter here
            sq = pull_board_square(coord)
            if idx == 0: continue # skip king's square
            # at last iteration
            elif idx == len(range(victim[0], r[0])) - 1 and sq.get("player") == None:
                protecting_guy = r # set this rook as the protecting_guy [THE BIG BRO!]
            if sq.get("player") == None:
                continue
            elif sq.get("player") == protector:
                break
            else: # sq = not protector
                break
        for idx, x in enumerate(range(r[0] , victim[0])): # rook is in left side of king
            coord = [x , victim[1]] # the y coord doesn't really matter here
            sq = pull_board_square(coord)
            if idx == 0: continue # skip king's square
            # at last iteration
            elif idx == len(range(r[0] , victim[0])) - 1 and sq.get("player") == None:
                protecting_guy = r # set this rook as the protecting_guy [THE BIG BRO!]
            if sq.get("player") == None:
                continue
            elif sq.get("player") == protector:
                break
            else: # sq = not protector
                break
        for idx, y in enumerate(range(r[1] , victim[1])): # rook is in up side of king
            coord = [victim[0], y] # the x coord doesn't really matter here
            sq = pull_board_square(coord)
            if idx == 0: continue # skip king's square
            # at last iteration
            elif idx == len(range(r[1] , victim[1])) - 1 and sq.get("player") == None:
                protecting_guy = r # set this rook as the protecting_guy [THE BIG BRO!]
            if sq.get("player") == None:
                continue
            elif sq.get("player") == protector:
                break
            else: # sq = not protector
                break
        for idx, y in enumerate(range(victim[1], r[1])): # rook is on down side of king
            coord = [victim[0], y] # the x coord doesn't really matter here
            sq = pull_board_square(coord)
            if idx == 0: continue # skip king's square
            # at last iteration
            elif idx == len(range(victim[1] , r[1])) - 1 and sq.get("player") == None:
                protecting_guy = r # set this rook as the protecting_guy [THE BIG BRO!]
            if sq.get("player") == None:
                continue
            elif sq.get("player") == protector:
                break
            else: # sq = not protector
                break
        if protecting_guy != None: # or `if not protecting_guy`    
            queen_protectors.append(protecting_guy) if queen_bandage_to_fn else rook_protectors.append(protecting_guy)
    for r in find_piece(player=protector, piece='r', output_format=list):
        # draw line and check path between just like pinned piece
        try:
            m = (r[1]-victim[1]) / (r[0]-victim[0])
            if m == 0: rook_eq_check_between(r=r) # m == 0, covers both 0deg and 180deg
        except ZeroDivisionError: # angle = 90deg or 270deg
            rook_eq_check_between(r=r)

    # 2. bishop
    def bishop_eq_check_between(b: list, queen_bandage_to_fn=False):
        """run check for both +x and -x the one which is not correct will drop out because of range() fn"""
        protecting_guy = None # just declared something
        for idx, x in enumerate(range(victim[0] , b[0])): # bishop is in right side of king
            coord = [x, victim[1] + idx] if victim[1] < b[1] else [x , victim[1] - idx] # again im a fucking genius
            sq = pull_board_square(coord)
            if idx == 0: continue # skip king's square
            # at last iteration
            elif idx == len(range(victim[0], b[0])) - 1 and sq.get("player") == None:
                protecting_guy = b # set this bishop as the protecting_guy [THE SNIPER!]
            if sq.get("player") == None:
                continue
            elif sq.get("player") == protector:
                break
            else: # sq = not player
                break
        for idx, x in enumerate(range(b[0] , victim[0])): # bishop is in left side of king
            coord = [x, victim[1] + 1] if victim[1] < b[1] else [x , victim[1] - 1] # again im a fucking genius
            sq = pull_board_square(coord)
            if idx == 0: continue # skip king's square
            # at last iteration
            elif idx == len(range(b[0], victim[0])) - 1 and sq.get("player") == None:
                protecting_guy = b # set this bishop as the protecting_guy [THE SNIPER!]
            if sq.get("player") == None:
                continue
            elif sq.get("player") == protector:
                break
            else: # sq = not player
                break
        if protecting_guy != None: # or `if not protecting_guy`
            queen_protectors.append(protecting_guy) if queen_bandage_to_fn else bishop_protectors.append(protecting_guy)
    for b in find_piece(player=protector, piece="b", output_format=list):
        # draw line to !player's king and check slope of the line
        m = (b[1]-victim[1]) / (b[0]-victim[0])
        if m in [-1 , 1]: bishop_eq_check_between(b=b)
    
    # 3. queen ......
    # queen = rook + bishop , so no fn needed this time sucker! 
    for q in find_piece(player=protector, piece="q", output_format=list):
        # draw line to !player's king and check slope of the line
        try:
            m = (q[1]-victim[1]) / (q[0]-victim[0])
            if m == 0: rook_eq_check_between(r=q, queen_bandage_to_fn=True) # rook
            elif m in [1, -1]: bishop_eq_check_between(b=q, queen_bandage_to_fn=True) # bishop
        except ZeroDivisionError:
            rook_eq_check_between(r=q) # rook with 90deg angle
    
    # 4. knight
    def kinght_squares(src):
        oCoords = [ [2,1] , [1,2] , [-1,2] , [-2,1] , [-2,-1] , [-1,-2] , [1,-2] , [2,-1] ]
        shiftedCoords = [
            [x + src[0], y + src[1]]
            for x, y in oCoords
            if (x + src[0] <= 8 and y + src[1] <= 8 and x + src[0] >= 1 and y + src[1] >= 1) # 1<=x,y<=8
        ]
        return shiftedCoords
    for n in find_piece(player=protector, piece='n', output_format=list):
        if cos in kinght_squares(src=n): # get the squares covering that specific knight
            knight_protectors.append(n) # add that knight to the protectors

    # 5. king
    def king_squares(src):
        oCoords = [[-1,1] , [0,1] , [1,1] , [1,0] , [1,-1] , [0,-1] , [-1,-1] , [-1,0]]
        shiftedCoords = [
            [x + src[0], y + src[1]]
            for x, y in oCoords
            if (x + src[0] <= 8 and y + src[1] <= 8 and x + src[0] >= 1 and y + src[1] >= 1) # 1<=x,y<=8
        ]
        return shiftedCoords
    for k in find_piece(player=protector, piece='k', output_format=list):
        if cos in king_squares(src=k): # get the squares covering that specific king
            king_protectors.append(k) # add that king to the protectors

    # 6. pawn
    def pawn_squares(src):
        oCoords = [[-1,1] , [1,1]] if protector else [[-1,-1], [1,-1]] # why not the forward step? 'cause that isnt the attacking sqaure of pawn
        shiftedCoords = [
            [x + src[0], y + src[1]]
            for x, y in oCoords
            if (x + src[0] <= 8 and y + src[1] <= 8 and x + src[0] >= 1 and y + src[1] >= 1) # 1<=x,y<=8
        ]
        return shiftedCoords
    for p in find_piece(player=protector, piece='p', output_format=list):
        if cos in pawn_squares(src=p): # get the squares covering that specific pwn
            pawn_protectors.append(p) # add that pawn to the protectors
    
    return {'r': rook_protectors,
            'n': knight_protectors,
            'b': bishop_protectors,
            'q': queen_protectors,
            'k': king_protectors,
            'p': pawn_protectors
        }

# pinned peice logic
def get_pinned_peices(player: bool):
    """
    returns the coords of piece and piece which are pinned for given player. 
    return format --> {"r": rook_pps, "b": bishop_pps, "q": queen_pps} if pps != [] else "huhhh no pps for him mate" # if there are no pinned pieces
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

    return {"r": rook_pps, "b": bishop_pps, "q": queen_pps} if pps != [] else "huhhh no pps for him mate" # if there are no pinned pieces

# check status
def am_i_in_check(player: bool):
    """ returns True if player is in check else False """
    p_king = find_piece(player=player, piece="k", output_format=list)[0]
    protectors = get_protectors(protector=not player, cos=p_king)
    total_attackers = sum(len(v) for v in protectors.values())
    return True if total_attackers > 0 else False

# pull up the possible moves of a piece, src[1]
def pull_possible_moves(player: bool, piece: str, src: list, dest: list):
    """
        how the heck this works?
        => first consider the piece is at origin (0,0) and hardcode the coords possible for the specific piece,
        then shift the origin at src pt and you have the possible moves after that we filter the paths by manualy going thtough all the board squares.
    """
    moves = []

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
                ((-1,  1), "-+")
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
        oCoords = [[-1,1] , [0,1] , [1,1]] if player else [[-1,-1], [0,-1] , [1,-1]] # had to do this because pawns can't walk backwards
        shiftedCoords = [
            [x + src[0], y + src[1]]
            for x, y in oCoords
            if (x + src[0] <= 8 and y + src[1] <= 8 and x + src[0] >= 1 and y + src[1] >= 1) # 1<=x,y<=8
        ]
        valid_moves = []
 
        for idx, pt in enumerate(shiftedCoords):
            d = pull_board_square(pt).get("player")
            if idx in [0 , 2] and d == (not player):
                valid_moves.append(pt) # capture move
            else:
                if d == None: valid_moves.append(pt) # move forward

        # if the pawn is at starting position (2nd or 7th depends) then this sucker can do a jump to 2 blocks
        adjacent_pawns = find_piece(player=not player, piece=piece, output_format=list) # player=false, piece='p' is the only case 
        if player and src[1] == 2: # white's pawn jumping 2 blocks
            valid_moves.append([src[0], 4])
            # enable en_passant for not player
            if [src[0]-1, 4] in adjacent_pawns: # left pawn (acc to white's pov)
                en_passant = {'for': False, 'to_capture': src, 'go_to': [src[0], src[1]-1]}
            elif [src[0]+1, 4] in adjacent_pawns: # right pawn (acc to white's pov)
                en_passant = {'for': False, 'to_capture': src, 'go_to': [src[0], src[1]-1]}
        elif (not player) and src[1] == 7: # black's pawn jumping 2 blocks
            valid_moves.append([src[0], 5])
            # en_passant
            if [src[0]-1, 5] in adjacent_pawns: # right pwn (acc to white's pov)
                en_passant = {'for': True, 'to_capture': src, 'go_to': [src[0], src[1]+1]}
            elif [src[0]+1, 4] in adjacent_pawns: # left pawn (acc to white's pov)
                en_passant = {'for': True, 'to_capture': src, 'go_to': [src[0], src[1]+1]}

        # en_passant (the illegal move noobs dont know about.)
        if en_passant["for"] == player: # im a fucking genius. only real ones can understand this 'if' part
            try:
                valid_moves.append(en_passant.get("go_to"))
                en_passant = None
            except Exception as e:
                print(f"error occured at en_passant code: \n{e}")

        return valid_moves

    def king_moves(player: bool):
        oCoords = [[-1,1] , [0,1] , [1,1] , [1,0] , [1,-1] , [0,-1] , [-1,-1] , [-1,0]]
        shiftedCoords = [
            [x + src[0], y + src[1]]
            for x, y in oCoords
            if (x + src[0] <= 8 and y + src[1] <= 8 and x + src[0] >= 1 and y + src[1] >= 1) # 1<=x,y<=8
        ] 
        valid_moves = []
        # blindly add squares then filter them later
        for pt in shiftedCoords:
            d = pull_board_square(pt).get("player")
            if d == player:
                continue
            elif d == (not player):
                valid_moves.append(pt)
            else:
                valid_moves.append(pt)
        
        # castling        
        if castleRights.get("w" if player else "b"):
            # if both consective squares are protected or players own piece reside there
            if not [src[0] + 1, src[1]] in get_protectors(protector=not player, cos=[src[0] + 1, src[1]]).values() or pull_board_square([src[0] + 1, src[1]]).get("player") == player:
                if not [src[0] + 2, src[1]] in get_protectors(protector=not player, cos=[src[0] + 2, src[1]]).values() or pull_board_square([src[0] + 2, src[1]]).get("player") == player:
                    # add that castling square sucker
                    valid_moves.append([src[0] + 2, src[1]])
                    # upadate var
                    if dest == [src[0] + 2, src[1]]:
                        castleRights = {"w": False if player else True, "b": False if not player else True}
            if not [src[0] - 1, src[1]] in get_protectors(protector=not player, cos=[src[0] - 1, src[1]]).values() or pull_board_square([src[0] - 1, src[1]]).get("player") == player:
                if not [src[0] + 2, src[1]] in get_protectors(protector=not player, cos=[src[0] - 2, src[1]]).values() or pull_board_square([src[0] - 2, src[1]]).get("player") == player:
                    # add that castling square sucker
                    valid_moves.append([src[0] - 2, src[1]])
                    # upadate var
                    if dest == [src[0] + 2, src[1]]:
                        castleRights = {"w": False if player else True, "b": False if not player else True}
        
        # rm castle rights if its just a normal move instead of castling before
        with open("./moves_sheet.txt" , "r") as RMS: # RMS -> readable move sheet. (don't judge the variable name)
            if f"{"w" if player else "b"} k" in RMS.read():
                castleRights = {"w": False if player else True, "b": False if not player else True}

        # remove the squares where there are protection by enemy
        for valid_move in valid_moves:
            for cosp in get_protectors(protector=not player, cos=valid_move).values(): # cosp -> coords of square protectors
                for coord in cosp:
                    try: valid_moves.remove(coord)
                    except ValueError: continue # at this point i m violetting the program to genrate error on purpose. Also Man specifying the ErrorType is brutal.

        return valid_moves
    
    def piece_switcher(player: bool, piece: str):
        match piece:
            case "r":
                return rook_moves(player)
            case "b":
                return bishop_moves(player)
            case "q":
                return queen_moves(player)
            case "n":
                return knight_moves(player)
            case "p":
                return pawn_moves(player)
            case "k":
                return king_moves(player)
            case _:
                raise ValueError("invalid piece type in piece_switcher fn")

    # if piece doesnt exist on src square then just stop this fn and send a 401
    if  not src in find_piece(player=player, piece=piece, output_format=list):
        return "bro really tried to play and illegal move, take this sucker (401)"
    # if the piece is pinned then stop the fn and send 401
    if src in get_pinned_peices(player=player).get(piece):
        return "bro really tried to play and illegal move, take this sucker (401) - pinned piece"

    # check for check
    if check == player:
        p_king = find_piece(player=player, piece="k", output_format=list)[0]
        protectors = get_protectors(protector=not player, cos=p_king)
        total_attackers = sum(len(v) for v in protectors.values())
        k_legal_moves = piece_switcher(player=player, piece="k") # get all possible moves of the player's king
        
        # checkmate condition
        if len(k_legal_moves) == 0 and total_attackers > 0:
            return f"{not player} checkmaated {player}!"
        # covering check condition
        if total_attackers == 1: # for good measure we could add `and piece != 'k'` here but its not neccessary because the piece will always be other than king if attackers == 1
            if piece == "k":
                return k_legal_moves # send the pre-calculated king moves rather than running piece_switcher fn again
            if piece != "k":
                tmp_board = board.copy() # backup the board
                place_piece(player=player, piece=piece, src=src, dest=dest) # for tmp purposes
                if am_i_in_check(player=player):
                    return "bro really tried to play and illegal move, take this sucker (401) - covering check"
                else: # the piece can cover the check
                    board = tmp_board.copy() # restore the board
                    del tmp_board # delete the backup
                    # set the check var to None because the check has been covered
                    check = None

                    # slow method but it works
                    # return piece_switcher(player=player, piece=piece) 
                    # send the bruteforced move
                    return [dest]
        # double check condition
        if total_attackers == 2:
            if piece != "k":
                return "bro really tried to play and illegal move, take this sucker (401) - double check"
            else:
                return k_legal_moves # send the pre-calculated king moves rather than running piece_switcher fn again

    # get the possible moves
    moves = piece_switcher(player=player, piece=piece)

    # setting the check var
    if dest in moves: # only if legal move
        tmp_board = board.copy() # backup the board
        place_piece(player=player, piece=piece, src=src, dest=dest) # for tmp purposes
        if am_i_in_check(player=not player): # when the player moves the piece then check was that check for (not player)
            check = not player
        else:
            check = None
    board = tmp_board.copy() # restore the board
    del tmp_board # delete the backup

    return moves

# moving a piece 
def move(ACN: str):
    # destructure acn
    dACN = ACN.split(" ") # acn => "w r d2 d4"
    # move data
    mData = {
        "player": True if dACN[0] == "w" else False,
        "piece": dACN[1] ,
        "src": dACN[2] ,
        "dest": dACN[3]
    }

    # get the possible moves
    possible_moves = pull_possible_moves(player=mData.get("player"), piece=mData.get("piece"), src=coords_convert(mData.get("src")), dest=coords_convert(mData.get("dest")))
    
    if type(possible_moves) == str: # error string from pull_possible_moves fn
        return possible_moves # its actually a str error message
    # move piece if dest in possible moves
    elif coords_convert(mData.get("dest")) in possible_moves:
        res = place_piece(player=mData.get("player"), piece=mData.get("piece"), src=coords_convert(mData.get("src")), dest=coords_convert(mData.get("dest")))
        
        # write move on sheet
        moves_sheet.write(f"{ACN}\n")
        
        if res == 200:
            return "piece moved successfully (200)"

def reset_board():
    """ resets the board to initial position """
    global board, check, en_passant, castleRights
    board = board_copy.copy()
    check = None
    en_passant = None
    castleRights = {"w": True, "b": True}