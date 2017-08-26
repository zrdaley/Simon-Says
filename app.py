import json
from random import randint

from flask import Flask, render_template, request
 
 
app = Flask(__name__)
app.debug = True

moves = []
users_score = 0

@app.route("/")
def simon_says():
	app.logger.info('/')
	return render_template('simon_says.html')

@app.route("/get-move", methods=['POST', 'GET'])
def get_move():
	global users_score
	app.logger.info('/get-move')
	data = json.loads(request.data)
	moves = data.get('moves')
	new_game = data.get('new')

	if new_game:
		users_score = 0

	moves.append(randint(1, 4))
	return json.dumps({'moves': moves, 'user': users_score})

@app.route("/check-move", methods=['POST'])
def check_move():
	global users_score
	app.logger.info('/check-move')
	data = json.loads(request.data)
	simons_moves = data.get('simons_moves')
	users_moves = data.get('moves')
	timeout = data.get('timeout')
	len_users_moves = len(users_moves)
	len_simons_moves = len(simons_moves)

	if len_users_moves == 0:
		return json.dumps({'valid': False, 'user': users_score})

	if timeout and len_users_moves < len_simons_moves:
		return json.dumps({'valid': False, 'user': users_score})

	# This shouldn't ever happen, but just to be safe
	if len_users_moves > len_simons_moves:
		return json.dumps({'valid': False, 'user': users_score})

	simons_moves = simons_moves[:len_users_moves]
	if simons_moves == users_moves:
		users_score += 1
		return json.dumps({'valid': True, 'user': users_score})
	return json.dumps({'valid': False, 'user': users_score})

 
if __name__ == "__main__":
	app.run()

