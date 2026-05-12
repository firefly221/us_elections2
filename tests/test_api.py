import tempfile
import unittest
from pathlib import Path

from app import create_app
from app.db import get_db, init_db


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        database_path = str(Path(self.tmpdir.name) / "test.sqlite3")
        self.app = create_app({"TESTING": True, "DATABASE_PATH": database_path})
        with self.app.app_context():
            init_db(drop=True)
        self.client = self.app.test_client()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_health_returns_ok(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_database_tables_are_created(self):
        with self.app.app_context():
            tables = get_db().execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()

        table_names = {table["name"] for table in tables}
        self.assertIn("voters", table_names)
        self.assertIn("candidates", table_names)

    def test_can_insert_candidate_and_voter(self):
        with self.app.app_context():
            db = get_db()
            db.execute("INSERT INTO candidates (name, party) VALUES (?, ?)", ("Jane", "Demo"))
            db.execute(
                "INSERT INTO voters (email, password_hash, name) VALUES (?, ?, ?)",
                ("alice@example.com", "hash", "Alice"),
            )
            db.commit()

            candidates = db.execute("SELECT COUNT(*) FROM candidates").fetchone()[0]
            voters = db.execute("SELECT COUNT(*) FROM voters").fetchone()[0]

        self.assertEqual(candidates, 1)
        self.assertEqual(voters, 1)


if __name__ == "__main__":
    unittest.main()
