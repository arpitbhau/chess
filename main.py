# radhe radhe

db = {
    "positions": {
        "a1":  {
            "own": "W",
            "reside": "r1"
        },
        "b1":  "kn1",
        "c1":  "b1",
        "d1":  "q",
        "e1":  "k",
        "f1":  "b2",
        "g1":  "kn2",
        "h1":  "r2",
        "a2":  "p1",
        "b2":  "p2",
        "c2":  "p3",
        "d2":  "p4",
        "e2":  "p5",
        "f2":  "p6",
        "g2":  "p7",
        "h2":  "p8",
        "a3":  None,
        "b3":  None,
        "c3":  None,
        "d3":  None,
        "e3":  None,
        "f3":  None,
        "g3":  None,
        "h3":  None,
        "a4":  None,
        "b4":  None,
        "c4":  None,
        "d4":  None,
        "e4":  None,
        "f4":  None,
        "g4":  None,
        "h4":  None,
        "a5":  None,
        "b5":  None,
        "c5":  None,
        "d5":  None,
        "e5":  None,
        "f5":  None,
        "g5":  None,
        "h5":  None,
        "a6":  None,
        "b6":  None,
        "c6":  None,
        "d6":  None,
        "e6":  None,
        "f6":  None,
        "g6":  None,
        "h6":  None,
        "a7":  "p1",
        "b7":  "p2",
        "c7":  "p3",
        "d7":  "p4",
        "e7":  "p5",
        "f7":  "p6",
        "g7":  "p7",
        "h7":  "p8",
        "a8":  "r1",
        "b8":  "kn1",
        "c8":  "b1",
        "d8":  "q",
        "e8":  "k",
        "f8":  "b2",
        "g8":  "kn2",
        "h8":  "r2"
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

            