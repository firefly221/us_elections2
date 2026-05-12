import sqlite3

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE_PATH"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(drop=False):
    db = get_db()

    if drop:
        db.executescript(
            """
            DROP TABLE IF EXISTS voters;
            DROP TABLE IF EXISTS candidates;
            """
        )

    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            party TEXT NOT NULL,
            votes INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS voters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0,
            voted INTEGER NOT NULL DEFAULT 0,
            candidate_id INTEGER,
            FOREIGN KEY (candidate_id) REFERENCES candidates(id)
        );
        """
    )
    db.commit()
