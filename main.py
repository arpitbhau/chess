# radhe radhe

db = {
    "positions": {
        "a1":  {
            "own": "W",
            "reside": "r"
        },
        "b1":  {
            "own": "W",
            "reside": "kn"
        },
        "c1":  {
            "own": "W",
            "reside": "b"
        },
        "d1":  {
            "own": "W",
            "reside": "q"
        },
        "e1":  {
            "own": "W",
            "reside": "k"
        },
        "f1":  {
            "own": "W",
            "reside": "b"
        },
        "g1":  {
            "own": "W",
            "reside": "kn"
        },
        "h1":  {
            "own": "W",
            "reside": "r"
        },
        "a2":  {
            "own": "W",
            "reside": "p"
        },
        "b2":  {
            "own": "W",
            "reside": "p"
        },
        "c2":  {
            "own": "W",
            "reside": "p"
        },
        "d2":  {
            "own": "W",
            "reside": "p"
        },
        "e2":  {
            "own": "W",
            "reside": "p"
        },
        "f2":  {
            "own": "W",
            "reside": "p"
        },
        "g2":  {
            "own": "W",
            "reside": "p"
        },
        "h2":  {
            "own": "W",
            "reside": "p"
        },
        "a3":  {
            "own": None,
            "reside": None
        },
        "b3":  {
            "own": None,
            "reside": None
        },
        "c3":  {
            "own": None,
            "reside": None
        },
        "d3":  {
            "own": None,
            "reside": None
        },
        "e3":  {
            "own": None,
            "reside": None
        },
        "f3":  {
            "own": None,
            "reside": None
        },
        "g3":  {
            "own": None,
            "reside": None
        },
        "h3":  {
            "own": None,
            "reside": None
        },
        "a4":  {
            "own": None,
            "reside": None
        },
        "b4":  {
            "own": None,
            "reside": None
        },
        "c4":  {
            "own": None,
            "reside": None
        },
        "d4":  {
            "own": None,
            "reside": None
        },
        "e4":  {
            "own": None,
            "reside": None
        },
        "f4":  {
            "own": None,
            "reside": None
        },
        "g4":  {
            "own": None,
            "reside": None
        },
        "h4":  {
            "own": None,
            "reside": None
        },
        "a5":  {
            "own": None,
            "reside": None
        },
        "b5":  {
            "own": None,
            "reside": None
        },
        "c5":  {
            "own": None,
            "reside": None
        },
        "d5":  {
            "own": None,
            "reside": None
        },
        "e5":  {
            "own": None,
            "reside": None
        },
        "f5":  {
            "own": None,
            "reside": None
        },
        "g5":  {
            "own": None,
            "reside": None
        },
        "h5":  {
            "own": None,
            "reside": None
        },
        "a6":  {
            "own": None,
            "reside": None
        },
        "b6":  {
            "own": None,
            "reside": None
        },
        "c6":  {
            "own": None,
            "reside": None
        },
        "d6":  {
            "own": None,
            "reside": None
        },
        "e6":  {
            "own": None,
            "reside": None
        },
        "f6":  {
            "own": None,
            "reside": None
        },
        "g6":  {
            "own": None,
            "reside": None
        },
        "h6":  {
            "own": None,
            "reside": None
        },
        "a7":  {
            "own": "B",
            "reside": "p"
        },
        "b7":  {
            "own": "B",
            "reside": "p"
        },
        "c7":  {
            "own": "B",
            "reside": "p"
        },
        "d7":  {
            "own": "B",
            "reside": "p"
        },
        "e7":  {
            "own": "B",
            "reside": "p"
        },
        "f7":  {
            "own": "B",
            "reside": "p"
        },
        "g7":  {
            "own": "B",
            "reside": "p"
        },
        "h7":  {
            "own": "B",
            "reside": "p"
        },
        "a8":  {
            "own": "B",
            "reside": "r"
        },
        "b8":  {
            "own": "B",
            "reside": "kn"
        },
        "c8":  {
            "own": "B",
            "reside": "b"
        },
        "d8":  {
            "own": "B",
            "reside": "q"
        },
        "e8":  {
            "own": "B",
            "reside": "k"
        },
        "f8":  {
            "own": "B",
            "reside": "b"
        },
        "g8":  {
            "own": "B",
            "reside": "kn"
        },
        "h8":  {
            "own": "B",
            "reside": "r"
        }
    }


}


class Chess:
    @staticmethod
    def chess_to_graph_coords(chess_coord):
        """
        Convert chess notation to graph coordinates.
        
        Args:
            chess_coord (str): Chess notation (e.g., 'a1', 'h8').
            
        Returns:
            tuple: Graph coordinates (x, y).
        """
        if len(chess_coord) != 2:
            raise ValueError("Invalid chess coordinate format. Use 'a1' to 'h8'.")
        
        file = ord(chess_coord[0]) - ord('a')  # Convert 'a' to 0, 'b' to 1, ..., 'h' to 7
        rank = int(chess_coord[1]) - 1          # Convert '1' to 0, ..., '8' to 7
        
        if not (0 <= file < 8 and 0 <= rank < 8):
            raise ValueError("Chess coordinate out of bounds. Use 'a1' to 'h8'.")
        
        return file+1 , rank+1 # Adjusting to 1-based indexing for graph coordinates

    @staticmethod
    def graph_to_chess_coords(graph_coord):
        """
        Convert graph coordinates to chess notation.
        
        Args:
            graph_coord (tuple): Graph coordinates (x, y).
            
        Returns:
            str: Chess notation (e.g., 'a1', 'h8').
        """
        if len(graph_coord) != 2:
            raise ValueError("Invalid graph coordinate format. Use (x, y) where x and y are integers from 0 to 7.")
        
        file, rank = graph_coord
        if not (0 <= file < 8 and 0 <= rank < 8):
            raise ValueError("Graph coordinate out of bounds. Use (0, 0) to (7, 7).")
        
        return f"{chr(file + ord('a') - 1)}{rank}"

    @staticmethod
    def destructure_ACN(ACN):
        """
        Helps destructuring the acn for further calculation

        Args:
            ACN / algebric chess notation (str): 
                 - "W/B p/r/Kn/b/k/q d2 d4 x/m"
                -- W/B => white or black moved
                -- pieces:
                    1. p - pawn
                    2. r - rook
                    3. Kn - knight
                    4. b - bishop
                    5. k - king
                    6. q - queen
                -- source
                -- destination
                -- takes (x) or moves (m)

        Returns:
            dict: {
                player: "" ,
                src: "",
                dest: "",
                tm: "x or m"
            }
        
        """
        ACN_arr = ACN.split(" ")

        return {
            "player": ACN_arr[0], # player who moved (W/B)
            "piece": ACN_arr[1], # piece type
            "src": ACN_arr[2], # source coordinate
            "dest": ACN_arr[3], # destination coordinate
            "takes": True if len(ACN_arr) > 4 else False # true if takes, false if moves
        }

    @staticmethod
    def legal_move(ACN):
        """
        Check if a move from src to dest is legal on a chessboard (basic bounds check).
        
        Args:
            src (str): src coordinate (e.g., 'a1').
            dest (str): dest coordinate (e.g., 'h8').
        
        Returns:
            bool: True if both coordinates are valid, False otherwise.
        """
        
        data = Chess.destructure_ACN(ACN)

        def rook_check(data): 
            p = data["p"]
            s = data["s"]
            d = data["d"]
            x = data["x"]


            src_coords = Chess.chess_to_graph_coords(s)
            dest_coords = Chess.chess_to_graph_coords(d)

            