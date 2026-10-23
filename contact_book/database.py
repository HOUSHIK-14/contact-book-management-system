"""SQLite data access for the Contact Book Management System."""
import sqlite3
from pathlib import Path
from typing import Optional

DEFAULT_DB = Path(__file__).resolve().parent.parent / "contact_book.db"


class ContactDatabase:
    def __init__(self, db_path=DEFAULT_DB):
        self.db_path = str(db_path)
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL UNIQUE,
                    email TEXT DEFAULT '',
                    address TEXT DEFAULT '',
                    category TEXT DEFAULT 'Other',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def add_contact(self, name, phone, email="", address="", category="Other"):
        with self._connect() as conn:
            cursor = conn.execute("""
                INSERT INTO contacts (name, phone, email, address, category)
                VALUES (?, ?, ?, ?, ?)
            """, (name.strip(), phone.strip(), email.strip(), address.strip(), category))
            return cursor.lastrowid

    def get_contacts(self, search=""):
        term = f"%{search.strip()}%"
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT contact_id, name, phone, email, address, category, created_at
                FROM contacts
                WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
                ORDER BY name COLLATE NOCASE
            """, (term, term, term)).fetchall()
            return [dict(row) for row in rows]

    def get_contact(self, contact_id):
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM contacts WHERE contact_id = ?", (contact_id,)
            ).fetchone()
            return dict(row) if row else None

    def update_contact(self, contact_id, name, phone, email="", address="", category="Other"):
        with self._connect() as conn:
            cursor = conn.execute("""
                UPDATE contacts
                SET name = ?, phone = ?, email = ?, address = ?, category = ?
                WHERE contact_id = ?
            """, (name.strip(), phone.strip(), email.strip(), address.strip(),
                  category, contact_id))
            return cursor.rowcount > 0

    def delete_contact(self, contact_id):
        with self._connect() as conn:
            cursor = conn.execute(
                "DELETE FROM contacts WHERE contact_id = ?", (contact_id,)
            )
            return cursor.rowcount > 0

    def count_contacts(self):
        with self._connect() as conn:
            return conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
