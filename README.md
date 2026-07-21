# 🔐 Password Manager

A lightweight desktop password manager built with **Python**, **Tkinter**, and **SQLite**. It helps everyday users generate strong, complex passwords and securely store, look up, edit, and delete their login credentials — all in a local database on their own machine.
<p align="center">
  <img src="Images/Screenshot 2026-07-21 184037.png" width="250">
  <img src="Images/Screenshot 2026-07-21 184256.png" width="250">
  <img src="Images/Screenshot 2026-07-21 184341.png" width="250">
</p>

## Why this project

Most people end up relying on third-party password managers, which means trusting yet another external company with the keys to their accounts. This app takes a different approach: a simple, self-contained, **local-only** solution where you're the one in charge of managing your own passwords — nothing is stored in the cloud or handled by a third party. It also includes a built-in password generator that suggests long, strong passwords, so you're never stuck reusing weak ones.

## Features

- **Master password login** — a single master password protects access to the app and is fundamental to how the encryption works
- **Password generation** — built-in algorithm suggests long, strong, randomized passwords
- **Credential storage** — save the site, username, and password to a local SQLite database
- **Lookup** — view all previously registered credentials in one place
- **Edit & delete** — modify or remove any stored entry
- **Fully local** — all data stays on your machine; nothing is sent over the network or handled by a third party

## Tech Stack

| Component | Technology |
|---|---|
| GUI | [Tkinter](https://docs.python.org/3/library/tkinter.html) |
| Database | [SQLite](https://www.sqlite.org/) |
| Language | Python |
| Encryption | Gauss-Jacques Algorithm |

### About the encryption

Stored password data is secured using the **Gauss-Jacques Algorithm**, developed in collaboration with [Dr. Fausto A. Jacques](https://www.linkedin.com/in/dr-fausto-a-jacques-7a6b6023b/).

## Project Structure

```
Password-Manager/
├── PswMkr.py        # Main application entry point / GUI logic
├── dba.py           # Database access layer (SQLite interactions)
├── Repository.db    # Local SQLite database
├── logo_icono.ico   # App icon
└── .vscode/         # Editor configuration
```

## Getting Started

### Option 1: Download the installer (recommended)

1. Go to the [Releases](https://github.com/Mancorb/Password-Manager/releases) page.
2. Download the latest `Ver X.X.exe` installer.
3. Run the installer — it bundles the executable, icon, and local database.

> **Note:** On first launch, your antivirus software may flag the app since it isn't code-signed. This is expected — the app runs entirely locally and doesn't transmit any data. You can safely allow it to run.

### Option 2: Run from source

**Requirements:**
- Python 3.x
- Tkinter (included with most standard Python installations)

```bash
# Clone the repository
git clone https://github.com/Mancorb/Password-Manager.git
cd Password-Manager

# Run the app
python PswMkr.py
```

## Compatibility

Currently supported on **Windows 8, 10, and 11**.

## Roadmap

This project is under active development. Planned improvements include:
- [ ] **Export/import** — export saved encrypted passwords to transfer them to a new device or migrate to another password manager
- [ ] **Login page redesign** — improve the UI/UX of the login screen
- [ ] **Version 2.0** — a Java-based desktop UI to bring macOS/Linux compatibility
- [ ] **Account recovery** — extend the encryption approach with a secondary access method for cases where the user forgets or loses their master password

## Contributing

Bug reports, feature requests, and suggestions are welcome! Please open an issue on the [Issues](https://github.com/Mancorb/Password-Manager/issues) page.

## Author

**Andres Emilio Miranda** ([@Mancorb](https://github.com/Mancorb))

## License

No license specified yet — all rights reserved by the author unless stated otherwise.
