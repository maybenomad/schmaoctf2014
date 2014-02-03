from schmao import app
from schmao.models import *
from flask import render_template, request, jsonify


GRID = [
	['Princess Tracker', '', 'Hitman', 'OooSQL'],
	['Wizards Only', '', 'flag_gen', 'Diary?'],
	['Gossip', 'Enc0ded', '', 'Unacceptable'],
	['Riddle', '', '', 'Imagination Machine']
]

challs = Challenge.query.all()
for row in range(4):
	for column in range(4):
		for entry in challs:
			if entry.name == GRID[row][column]:
				GRID[row][column] = entry

@app.route("/")
def index():
	return render_template('tasks.html', grid=GRID)

@app.route("/solve")
def solve():
	flag = request.args.get('flag', None)
	name = request.args.get('name', None)

	for chall in challs:
		if chall.name == name:
			if chall.flag == flag:
				return jsonify(solved=True)
	return jsonify(solved=False)

@app.route('/task')
def task():
	name = request.args.get('name', None)
	for chall in challs:
		if chall.name == name:
			return jsonify(name=chall.name, desc=chall.desc, 
				category=chall.category.lower())