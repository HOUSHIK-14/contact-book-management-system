"""Tkinter graphical interface."""
import csv
import re
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from .database import ContactDatabase

CATEGORIES = ("Family", "Friend", "Work", "College", "Other")


class ContactBookApp(tk.Tk):
    def __init__(self, database=None):
        super().__init__()
        self.db = database or ContactDatabase()
        self.title("Contact Book Management System")
        self.geometry("1060x680")
        self.minsize(900, 580)
        self.configure(bg="#f3f6fb")
        self.selected_id = None
        self.vars = {
            "name": tk.StringVar(),
            "phone": tk.StringVar(),
            "email": tk.StringVar(),
            "address": tk.StringVar(),
            "category": tk.StringVar(value="Other"),
            "search": tk.StringVar(),
        }
        self._style()
        self._build_ui()
        self.refresh_contacts()

    def _style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=29, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=7)
        style.configure("TLabel", background="#ffffff", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#1f3b73", foreground="white",
                        font=("Segoe UI", 20, "bold"))
        style.configure("Sub.TLabel", background="#1f3b73", foreground="#dce7ff",
                        font=("Segoe UI", 10))

    def _build_ui(self):
        header = tk.Frame(self, bg="#1f3b73", padx=22, pady=18)
        header.pack(fill="x")
        ttk.Label(header, text="Contact Book Management System",
                  style="Header.TLabel").pack(anchor="w")
        ttk.Label(header, text="Save, search and manage your contacts in one place",
                  style="Sub.TLabel").pack(anchor="w", pady=(4, 0))

        content = tk.Frame(self, bg="#f3f6fb", padx=18, pady=16)
        content.pack(fill="both", expand=True)

        form = tk.LabelFrame(content, text=" Contact Details ", bg="white",
                             padx=14, pady=12, font=("Segoe UI", 11, "bold"))
        form.pack(fill="x", pady=(0, 14))

        fields = [
            ("Full name *", "name", 0, 0),
            ("Phone number *", "phone", 0, 2),
            ("Email", "email", 1, 0),
            ("Address", "address", 1, 2),
        ]
        for label, key, row, col in fields:
            tk.Label(form, text=label, bg="white", font=("Segoe UI", 10)).grid(
                row=row, column=col, sticky="w", padx=(0, 8), pady=7)
            entry = ttk.Entry(form, textvariable=self.vars[key], width=34)
            entry.grid(row=row, column=col + 1, sticky="ew", padx=(0, 18), pady=7)
        tk.Label(form, text="Category", bg="white", font=("Segoe UI", 10)).grid(
            row=2, column=0, sticky="w", padx=(0, 8), pady=7)
        ttk.Combobox(form, textvariable=self.vars["category"], values=CATEGORIES,
                     state="readonly", width=31).grid(
            row=2, column=1, sticky="ew", padx=(0, 18), pady=7)
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        buttons = tk.Frame(form, bg="white")
        buttons.grid(row=2, column=2, columnspan=2, sticky="e", pady=4)
        ttk.Button(buttons, text="Add Contact", command=self.add_contact).pack(side="left", padx=3)
        ttk.Button(buttons, text="Update Selected", command=self.update_contact).pack(side="left", padx=3)
        ttk.Button(buttons, text="Clear", command=self.clear_form).pack(side="left", padx=3)

        listing = tk.Frame(content, bg="white", padx=12, pady=12)
        listing.pack(fill="both", expand=True)
        top = tk.Frame(listing, bg="white")
        top.pack(fill="x", pady=(0, 10))
        tk.Label(top, text="Saved Contacts", bg="white",
                 font=("Segoe UI", 13, "bold")).pack(side="left")
        ttk.Entry(top, textvariable=self.vars["search"], width=30).pack(
            side="right", padx=(8, 0))
        ttk.Button(top, text="Search", command=self.refresh_contacts).pack(side="right")
        ttk.Button(top, text="Show All", command=self.show_all).pack(side="right", padx=5)

        columns = ("id", "name", "phone", "email", "address", "category")
        self.tree = ttk.Treeview(listing, columns=columns, show="headings", selectmode="browse")
        headings = {
            "id": "ID", "name": "Name", "phone": "Phone",
            "email": "Email", "address": "Address", "category": "Category"
        }
        widths = {"id": 48, "name": 160, "phone": 120, "email": 190,
                  "address": 250, "category": 100}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], minwidth=45,
                             anchor="w" if col != "id" else "center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        bottom = tk.Frame(listing, bg="white")
        bottom.pack(fill="x", pady=(10, 0))
        ttk.Button(bottom, text="Delete Selected", command=self.delete_contact).pack(side="left")
        ttk.Button(bottom, text="Export CSV", command=self.export_csv).pack(side="left", padx=8)
        self.status = tk.Label(bottom, text="", bg="white", fg="#52627a",
                               font=("Segoe UI", 9))
        self.status.pack(side="right")

    def _validate(self):
        name = self.vars["name"].get().strip()
        phone = self.vars["phone"].get().strip()
        email = self.vars["email"].get().strip()
        if not name:
            messagebox.showwarning("Validation", "Please enter the contact's name.")
            return False
        digits = re.sub(r"\D", "", phone)
        if len(digits) != 10 or not phone.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            messagebox.showwarning("Validation", "Enter a valid 10-digit phone number.")
            return False
        if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            messagebox.showwarning("Validation", "Enter a valid email address.")
            return False
        return True

    def _form_values(self):
        return tuple(self.vars[k].get().strip() for k in
                     ("name", "phone", "email", "address", "category"))

    def add_contact(self):
        if not self._validate():
            return
        try:
            self.db.add_contact(*self._form_values())
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate phone", "A contact with this phone number already exists.")
            return
        self.clear_form()
        self.refresh_contacts()
        messagebox.showinfo("Success", "Contact added successfully.")

    def update_contact(self):
        if self.selected_id is None:
            messagebox.showwarning("Select contact", "Select a contact from the list first.")
            return
        if not self._validate():
            return
        try:
            self.db.update_contact(self.selected_id, *self._form_values())
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate phone", "Another contact already uses this phone number.")
            return
        self.clear_form()
        self.refresh_contacts()
        messagebox.showinfo("Success", "Contact updated successfully.")

    def delete_contact(self):
        if self.selected_id is None:
            messagebox.showwarning("Select contact", "Select a contact from the list first.")
            return
        if messagebox.askyesno("Confirm deletion", "Delete the selected contact?"):
            self.db.delete_contact(self.selected_id)
            self.clear_form()
            self.refresh_contacts()

    def clear_form(self):
        self.selected_id = None
        for key in ("name", "phone", "email", "address"):
            self.vars[key].set("")
        self.vars["category"].set("Other")
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def show_all(self):
        self.vars["search"].set("")
        self.refresh_contacts()

    def refresh_contacts(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        contacts = self.db.get_contacts(self.vars["search"].get())
        for c in contacts:
            self.tree.insert("", "end", values=(
                c["contact_id"], c["name"], c["phone"], c["email"],
                c["address"], c["category"]
            ))
        self.status.config(text=f"{len(contacts)} contact(s) shown")

    def _on_select(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.selected_id = int(values[0])
        contact = self.db.get_contact(self.selected_id)
        if contact:
            for key in ("name", "phone", "email", "address", "category"):
                self.vars[key].set(contact.get(key, "") or "")

    def export_csv(self):
        contacts = self.db.get_contacts(self.vars["search"].get())
        if not contacts:
            messagebox.showinfo("Export", "There are no contacts to export.")
            return
        path = filedialog.asksaveasfilename(
            title="Export contacts", defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")], initialfile="contacts.csv")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=[
                "contact_id", "name", "phone", "email", "address", "category", "created_at"
            ])
            writer.writeheader()
            writer.writerows(contacts)
        messagebox.showinfo("Export complete", f"Contacts exported to:\n{path}")
