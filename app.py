import json
from random import randint

from flask import Flask, render_template, request
 
 
app = Flask(__name__)
app.debug = True

moves = []
 
@app.route("/")
def simon_says():
	app.logger.info('/')
	return render_template('simon_says.html')

@app.route("/get-move", methods=['POST', 'GET'])
def get_move():
	app.logger.info('/get-move')
	data = json.loads(request.data)
	moves = data.get('moves')
	moves.append(randint(1, 4))
	return json.dumps(moves)

@app.route("/check-move", methods=['POST'])
def check_move():
	app.logger.info('/check-move')
	data = json.loads(request.data)
	simons_moves = data.get('simons_moves')
	users_moves = data.get('moves')

	app.logger.info(simons_moves)
	app.logger.info(users_moves)

	# This shouldn't ever happen, but just to be safe
	len_users_moves = len(users_moves)
	len_simons_moves = len(simons_moves)
	if len_users_moves > len_simons_moves:
		return json.dumps({'valid': False})


	simons_moves = simons_moves[:len_users_moves]
	if simons_moves == users_moves:
		return json.dumps({'valid': True})
	return json.dumps({'valid': False})


 
if __name__ == "__main__":
	app.run()



# request {
# 	'moves'
# 	'timeout'
# }

# return {
# 	'moves': [],
# 	'timeout': 5s min-20s max,
# }
