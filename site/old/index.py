from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/tasks")
def tasks():
	return render_template('tasks.html')

@app.route("/tasks/<taskname>")
def taskpages(taskname):
	return render_template('taskpage.html')

@app.route("/scoreboard")
def scoreboard():
	pass

if __name__ == "__main__":
  app.run(debug=True)
