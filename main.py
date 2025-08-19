# radhe radhe

import math , json


# read the db
global db
def read_db(f):
    try:
        with open(f , 'r') as file:
            return json.load(file) 
    except FileNotFoundError:
        print(f"Error: The file '{f}' was not found.")
        exit()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}") 
        exit()

db = read_db("db.json")

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

