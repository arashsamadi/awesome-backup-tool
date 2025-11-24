# Awesome Backup Tool

A lightweight and reliable incremental backup tool written in Python.  
It tracks file changes, copies only updated files, and moves deleted files into a timestamped archive. Perfect for academics, developers, and anyone who wants a simple backup solution.

---

## 📌 Features

- 🔄 **Incremental backup** — only new or modified files are copied  
- 🧹 **Deleted file tracking** — removed files are archived instead of lost  
- 🕒 **Metadata-based change detection**  
- 📁 **Folder structure preserved**  
- 🖥️ **Cross-platform** (Windows, Linux, macOS)  
- ⚡ **No external dependencies** — works with pure Python  

---
## ⚠️ Safety Notes

- Make sure the destination folder is correct to avoid overwriting important data
- The tool only moves deleted files, it does not automatically restore them
- You can run a “dry run” by copying the script and manually commenting out the safe_copy and shutil.move lines to preview what would happen

---
## 📝 Usage

Run the backup tool using the command-line interface:
```
py backup_v2.py --source "C:/path/to/source" --destination "D:/path/to/backup"
```

Or using short options:
```
py backup_v2.py -s "C:/path/to/source" -d "D:/path/to/backup"
```
Example (the command I personally use):
```
py .\backup_v2.py -s "C:/Users/Arash/Desktop/Academic" -d "G:/theAcademicBackup"
```

This will:

Copy all new or updated files from the source folder

Preserve the folder structure in the backup destination

Move deleted files into a timestamped deleted folder inside the backup directory

Save metadata in backup_metadata.json to track changes
## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/arashsamadi/awesome-backup-tool.git
cd awesome-backup-tool

