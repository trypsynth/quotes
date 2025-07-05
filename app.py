import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_basicauth import BasicAuth

import db

load_dotenv()
app = Flask(__name__)
app.config["BASIC_AUTH_USERNAME"] = os.environ.get("BASIC_AUTH_USERNAME")
app.config["BASIC_AUTH_PASSWORD"] = os.environ.get("BASIC_AUTH_PASSWORD")
basic_auth = BasicAuth(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quotes.db"
db.db.init_app(app)


@app.route("/", methods=["GET", "POST"])
@basic_auth.required
def index():
	if request.method == "POST":
		who = request.form["who"]
		quote = request.form["quote"]
		context = request.form.get("context", "")
		db.insert_quote(who, quote, context)
	quotes = db.get_quotes()
	return render_template("index.html", quotes=quotes)


if __name__ == "__main__":
	with app.app_context():
		db.setup()
	app.run()
