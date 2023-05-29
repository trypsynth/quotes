import sqlite3
from dataclasses import dataclass


@dataclass
class Quote:
    who: str
    quote: str
    context: str = ""


def setup():
    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS quotes (id INTEGER PRIMARY KEY AUTOINCREMENT, who TEXT, quote TEXT, context TEXT)"""
    )
    conn.commit()
    conn.close()


def insert_quote(who, quote, context):
    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO quotes (who, quote, context) VALUES (?, ?, ?)",
        (who, quote, context),
    )
    conn.commit()
    conn.close()


def get_quotes():
    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()
    c.execute("SELECT who, quote, context FROM quotes")
    quotes = [Quote(*row) for row in c.fetchall()]
    conn.close()
    return quotes
