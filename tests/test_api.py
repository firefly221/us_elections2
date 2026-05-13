import tempfile
import unittest
from pathlib import Path

from app import create_app
from app.db import init_db


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

    def register(self, email="Alice@example.com"):
        return self.client.post(
            "/api/auth/register",
            json={
                "name": "Alice Voter",
                "email": email,
                "password": "strongpass123",
                "confirm_password": "strongpass123",
            },
        )

    def test_register_creates_voter(self):
        response = self.register()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["voter"]["email"], "alice@example.com")

    def test_first_registered_user_is_admin(self):
        response = self.register()

        self.assertTrue(response.get_json()["voter"]["is_admin"])

    def test_duplicate_email_is_rejected(self):
        self.register()
        response = self.register(email="alice@example.com")

        self.assertEqual(response.status_code, 409)

    def test_invalid_registration_is_rejected(self):
        response = self.client.post(
            "/api/auth/register",
            json={
                "name": "",
                "email": "bad-email",
                "password": "short",
                "confirm_password": "different",
            },
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
