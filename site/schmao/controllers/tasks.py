from schmao import app
from schmao.models import *
from schmao import db
from flask import render_template, request,\
		jsonify, session, redirect, url_for


grid = ['Gossip', 'Enc0ded', 'Wenkbot', 'Imagination Machine', 
				'Diary?', 'http://iceking.wenk', 'Selfie', 'Riddle', 
				'Bad Cookie', 'Wizards Only', 'flag_gen','Hitman', 
				'Marceline', 'Princess Tracker', 'Unacceptable', 'OooSQL']

#####
#
# Query sorting helpers. 
#
#####
def gridify(chall):
	return grid.index(chall.name)

def points(user):
	total = 0
	for flag in user.flags:
		total += flag.points
	user.points = total
	return points

def pluck_user(coll, name):
	for item in coll:
		if item.name == name:
			return item

def flag_names(flags):
	return map(lambda x: x.name, flags)


@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "GET":
		if 'username' not in session:
			return render_template('login.html')
		else:
			# Retrieve scoreboard and challenge information. 
			challs = sorted(Challenge.query.all(), key=gridify)
			users = sorted(User.query.all(), key=points)

			# Collect current user's information
			me = pluck_user(users, session['username'])
			my_flags = flag_names(me.flags)

			return render_template('tasks.html', 
				challs=challs, users=users, my_flags=my_flags, me=me)
	else:
		# Valid POST will be login or register, should have username
		if 'username' in request.form:
			username = request.form['username']
			user = User.query.filter_by(name=username).first()

			if 'login' in request.form:
				if user:
					session['username'] = username

			elif 'register' in request.form:
				if not user:
					new = User(username)
					db.session.add(new)
					db.session.commit()
					session['username'] = username

	return redirect(url_for('index'))

@app.route("/solve")
def solve():
	flag = request.args.get('flag', None)
	name = request.args.get('name', None)
	user = User.query.filter_by(name=session['username']).first()

	challs = Challenge.query.all()
	if name not in flag_names(user.flags):
		for chall in challs:
			if chall.name == name:
				if chall.flag == flag:
						user.flags.append(chall)
						db.session.commit()
						return jsonify(solved=True)
	return jsonify(solved=False)

@app.route('/task')
def task():
	name = request.args.get('name', None)
	print name
	challs = Challenge.query.all()
	for chall in challs:
		if chall.name == name:
			return jsonify(name=chall.name, desc=chall.desc, 
				category=chall.category.lower())
	return jsonify(name='', desc='', category='')
