from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    who = db.Column(db.String(255), nullable=False)
    quote = db.Column(db.Text, nullable=False)
    context = db.Column(db.Text, nullable=False, default="")


def setup():
    db.create_all()


def insert_quote(who, quote, context):
    new_quote = Quote(who=who, quote=quote, context=context)
    db.session.add(new_quote)
    db.session.commit()


def get_quotes():
    return Quote.query.all()
