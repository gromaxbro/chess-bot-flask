import chess
import chess.engine

STOCKFISH_PATH = "/home/booster/Downloads/stockfish/stockfish-ubuntu-x86-64"

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

engine.configure({"Skill Level": 2})  # 0 = weakest, 20 = strongest

print("Play against Stockfish! Type algebraic moves (e.g., e4, Nf3). Type 'quit' to exit.\n")

while not board.is_game_over():
    move_input = input("Your move: ").strip()
    print(move_input)
    try:
        move = board.parse_san(move_input)
        print(move)
        board.push(move)
    except Exception:
        print("Invalid move. Example: e4, Nf3, exd5")
        continue

    if board.is_game_over():
        break

    # Stockfish move
    result = engine.play(board, chess.engine.Limit(time=1.0))
    bot_move = result.move
    board.push(bot_move)

    # Print move in UCI format to avoid SAN errors
    print("Stockfish plays (UCI):",bot_move.uci())

print("Game over! Result:", board.result())
engine.quit()
