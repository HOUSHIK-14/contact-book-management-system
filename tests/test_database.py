import tempfile
import unittest
from pathlib import Path

from contact_book.database import ContactDatabase


class ContactDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db = ContactDatabase(Path(self.temp_dir.name) / "test.db")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_search_contact(self):
        self.db.add_contact("Houshik", "9876543210", "houshik@example.com", "Coimbatore", "College")
        results = self.db.get_contacts("Houshik")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["phone"], "9876543210")

    def test_update_contact(self):
        contact_id = self.db.add_contact("Arun", "9123456780")
        self.db.update_contact(contact_id, "Arun Kumar", "9123456780", category="Friend")
        self.assertEqual(self.db.get_contact(contact_id)["name"], "Arun Kumar")

    def test_delete_contact(self):
        contact_id = self.db.add_contact("Priya", "9000011111")
        self.assertTrue(self.db.delete_contact(contact_id))
        self.assertIsNone(self.db.get_contact(contact_id))


if __name__ == "__main__":
    unittest.main()
