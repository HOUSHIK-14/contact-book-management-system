# Contact Book Management System

A Python desktop application for storing, searching, updating, deleting, and exporting contact details. It uses **Tkinter** for the graphical interface and **SQLite** for persistent local storage.

## Features

- Add contacts with name, phone, email, address, and category
- Search by name, phone number, or email
- Update and delete saved contacts
- Validate required fields, phone numbers, and email addresses
- Prevent duplicate phone numbers
- Sort contacts alphabetically
- Export contacts to a CSV file
- Keep contacts in a local SQLite database between sessions

## Technology stack

- Python 3.10+
- Tkinter (included with most standard Python installations)
- SQLite (included with Python)
- CSV module (Python standard library)

No third-party Python packages are required.

## Project structure

```text
contact-book-management-system/
├── main.py
├── contact_book/
│   ├── __init__.py
│   ├── database.py
│   └── gui.py
├── tests/
│   └── test_database.py
├── .gitignore
├── LICENSE
└── README.md
```

## Requirements

Install Python 3.10 or later. On Windows, select **Add Python to PATH** during installation.

Check the installation:

```bash
python --version
```

If that command does not work on Windows, try:

```bash
py --version
```

## Run the application

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Start the application:

```bash
python main.py
```

On Windows, this can also be:

```bash
py main.py
```

The SQLite database file `contact_book.db` is created automatically in the project folder when the application first runs.

## How to use

1. Enter a name and a 10-digit phone number.
2. Optionally enter email, address, and category.
3. Click **Add Contact**.
4. Select a saved row to load its details into the form.
5. Use **Update Selected** or **Delete Selected** to maintain a contact.
6. Search by name, phone, or email using the search field.
7. Click **Export CSV** to save the currently displayed contacts.

## Run tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

## Database schema

The `contacts` table includes:

| Field | Type | Description |
|---|---|---|
| `contact_id` | INTEGER | Auto-increment primary key |
| `name` | TEXT | Required contact name |
| `phone` | TEXT | Required, unique phone number |
| `email` | TEXT | Optional email |
| `address` | TEXT | Optional address |
| `category` | TEXT | Family, Friend, Work, College, or Other |
| `created_at` | DATETIME | Record creation timestamp |

## Limitations and future improvements

- This version stores data locally on one computer.
- The database is not encrypted; avoid storing highly sensitive information.
- Cloud synchronisation, user login, encrypted backups, import from vCard, and a mobile companion app could be added later.

## GitHub upload

Create a new **public** repository on GitHub named `contact-book-management-system`. Do not initialize it with a README if you already have this project's README.

Then run these commands from the project folder (replace the URL with your repository URL):

```bash
git init
git add .
git commit -m "Initial commit: Contact Book Management System"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/contact-book-management-system.git
git push -u origin main
```

Do not upload personal contact data or the generated `contact_book.db` file.
