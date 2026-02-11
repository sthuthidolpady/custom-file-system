# Custom File System Project

#Overview

This project is a **Custom File System Simulation** built using Python.  
It provides both:

-  GUI (Graphical User Interface)
- TUI (Terminal User Interface)

The system supports basic file operations like:

- Create
- Read
- Write
- Delete
- Rename
- View Properties
- Persistent Storage

---
file_system_project/
│
├── backend/
│ ├── file_system.py
│ ├── inode.py
│ ├── block.py
│ ├── storage.py
│ ├── fs_core.py
│ ├── fs_commands.py
│ └── fs_tui.py
│
├── ui/
│ └── gui.py
│
├── fs_state.pkl
├── fs_state.json
└── README.md


---

 Features

 CRUD Operations
- Create new files
- Read file content
- Write data to file
- Delete files
- Rename files

 File Properties
- Filename
- Size
- Blocks used
- Created time
- Modified time
- Accessed time
- Permissions

 Persistent Storage
All files are saved using serialization (`pickle`).
Even after closing the program, files remain stored.

---


