from flask import Flask,render_template,request, jsonify
import chess
import chess.engine
from pyngrok import ngrok
import requests
public_url = ngrok.connect(5000)
print("Ngrok tunnel URL:", public_url)
urll = str(public_url).split("https://")[1].split('" ->')[0]
# host_only = str(public_url).replace("https://", "").replace("http://", "").split('/')[0]
print(urll)
requests.get(f"https://zapet.fun/change/{urll}/yessir")

STOCKFISH_PATH = "/home/booster/Downloads/stockfish/stockfish-ubuntu-x86-64"

app = Flask(__name__,static_folder="static",static_url_path="/")

engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

board = chess.Board()

engine.configure({"Skill Level": 2})  # 0 = weakest, 20 = strongest


@app.route("/")
def index():
	return render_template("index.html")


def play(move_input):
	try:
		move = board.parse_san(move_input)
		board.push(move)
	except Exception:
		return "Invalid move"
	if board.is_game_over():
	    return "over"

	result = engine.play(board, chess.engine.Limit(time=2.0))
	bot_move = result.move
	board.push(bot_move)

	return bot_move.uci()


@app.route("/game_over")
def over():
	return "its over pls go again to site :)"

@app.route("/move", methods=['POST'])
def mob():
	# move_input = input("Your move: ").strip()
    data = request.get_json()
    piece = data.get('piece')
    note = data.get('note')
    tile = data.get('tile')
    if "P" == piece:
    	move_input = tile
    else:
    	move_input = piece+tile

    computer = play(move_input)
    if computer == "over":
    	return redirect("/game_over")


    print(f"Received move: {piece+tile}")
    print(f"computer move :{computer}")
    return computer

@app.route("/move-form", methods=['POST'])
def mobb():
	# move_input = input("Your move: ").strip()
    data = request.get_json()
    move_input = data.get('move')
    computer = play(move_input)

    print(f"computer move :{computer}")
    return computer


@app.route("/restart", methods=['POST'])
def ress():
    global board
    board = chess.Board()
    data = request.get_json()
    skill = data.get('skill', 2)  # default to 2 if not provided
    try:
        skill = int(skill)
    except ValueError:
        skill = 2

    engine.configure({"Skill Level": skill})

    return jsonify({"status": "restarted", "skill": skill})


if __name__ == '__main__':
	app.run()
