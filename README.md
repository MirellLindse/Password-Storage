[Русский](README.en.md) | [Eesti](README.et.md)

# 🔐 Password Storage And Generation App (PSAGA)

A small desktop application for securely storing passwords. Built using Python, PySide6, and SQLite. All passwords are encrypted before saving and can be conveniently copied to the clipboard with one button.

## 🧠 Project Goal

The goal is to create a simple yet functional password manager that:

- Safely stores passwords using symmetric encryption
- Allows copying passwords with a single button
- Deletes records both from the interface and the database
- Includes pagination and has a simple design
- Works entirely offline, with no internet connection required

## 💡 Features

- 🧷 Stores a `website / email / nickname / password` pair
- 🔒 Encrypts and decrypts passwords on the fly
- 👁 Only shows asterisks — security comes first
- 📋 "Copy" button next to each record for quick password copying
- 🗑 Deletes records with complete removal from the database
- 📄 Pagination for easy navigation through large sets of records

## 🧰 Tech Stack

- Python 3.x
- PySide6 (Qt for GUI)
- SQLite3 (embedded database)
- Fernet (from the cryptography library for encryption)

## 🖼 Screenshots

(In progress)

## 🚀 Project Setup

1. Clone the repository:

```bash
git clone https://github.com/MirellLindse/Pasword-Storage.git
