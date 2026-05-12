import os
from pathlib import Path

from flask import Flask, jsonify

from .db import close_db, init_db
from .routes import api


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["DATABASE_PATH"] = os.environ.get(
        "DATABASE_PATH",
        str(Path(__file__).resolve().parent.parent / "instance" / "uselections.sqlite3"),
    )

    if test_config:
        app.config.update(test_config)

    app.teardown_appcontext(close_db)
    app.register_blueprint(api)

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "not_found"}), 404

    Path(app.config["DATABASE_PATH"]).parent.mkdir(parents=True, exist_ok=True)
    with app.app_context():
        init_db()

    return app
