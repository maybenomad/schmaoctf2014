from flask import *
import os
import base64

app = Flask(__name__)

@app.before_request
def before_request():
	pass

@app.route("/")
def index():
	status = request.cookies.get("status")
	if status != None and base64.b64decode(status) == "wizard":
		print "Hit here"
		return render_template('index.html', flag="wizards only fools")
	resp = make_response(render_template('index.html'))
	resp.set_cookie('status', base64.b64encode("not_wizard"))
	return resp

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=False)