import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_basicauth import BasicAuth
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
app = Flask(__name__)
app.config["BASIC_AUTH_USERNAME"] = os.environ.get("BASIC_AUTH_USERNAME")
app.config["BASIC_AUTH_PASSWORD"] = os.environ.get("BASIC_AUTH_PASSWORD")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quotes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
basic_auth = BasicAuth(app)


class Quote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	who = db.Column(db.String(255), nullable=False)
	quote = db.Column(db.Text, nullable=False)
	context = db.Column(db.Text, nullable=False, default="")

	def __init__(self, who: str, quote: str, context: str = "") -> None:
		self.who = who
		self.quote = quote
		self.context = context


def insert_quote(who: str, quote: str, context: str) -> None:
	"""Insert a new quote into the database."""
	new_quote = Quote(who=who, quote=quote, context=context)
	db.session.add(new_quote)
	db.session.commit()


def get_quotes() -> list[Quote]:
	"""Get all quotes from the database."""
	return Quote.query.all()


@app.route("/", methods=["GET", "POST"])
@basic_auth.required
def index() -> str:
	if request.method == "POST":
		who = request.form["who"]
		quote = request.form["quote"]
		context = request.form.get("context", "")
		insert_quote(who, quote, context)
	quotes = get_quotes()
	return render_template("index.html", quotes=quotes)


if __name__ == "__main__":
	with app.app_context():
		db.create_all()
	app.run()
