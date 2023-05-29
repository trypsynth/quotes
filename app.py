from flask import Flask, render_template, request
import db

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        who = request.form["who"]
        quote = request.form["quote"]
        context = request.form.get("context", "")
        db.insert_quote(who, quote, context)
    quotes = db.get_quotes()
    return render_template("index.html", quotes=quotes)


if __name__ == "__main__":
    db.setup()
    app.run()
