import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_basicauth import BasicAuth
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
app = Flask(__name__)
app.config["BASIC_AUTH_USERNAME"] = os.environ.get("BASIC_AUTH_USERNAME")
app.config["BASIC_AUTH_PASSWORD"] = os.environ.get("BASIC_AUTH_PASSWORD")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///quotes.db")
db = SQLAlchemy(app)
basic_auth = BasicAuth(app)

with app.app_context():
	db.create_all()


class Quote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	who = db.Column(db.String(255), nullable=False)
	quote = db.Column(db.Text, nullable=False)
	context = db.Column(db.Text, nullable=False, default="")


@app.route("/", methods=["GET", "POST"])
@basic_auth.required
def index() -> str:
	if request.method == "POST":
		db.session.add(Quote(
			who=request.form["who"],
			quote=request.form["quote"],
			context=request.form.get("context", ""),
		))
		db.session.commit()
		return redirect(url_for("index"))
	quotes = db.session.execute(db.select(Quote)).scalars().all()
	return render_template("index.html", quotes=quotes)


if __name__ == "__main__":
	app.run()
