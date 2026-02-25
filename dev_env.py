# radhe radhe
import main_game

while True:
    move_str = input("move: ")
    if move_str == ":b":
        main_game.pretty_board()
    elif move_str == ":r":
        main_game.reset_board()
    else:
        res = main_game.move(move_str)
        print(res.get("status"))
