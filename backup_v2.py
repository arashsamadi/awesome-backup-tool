import os
import shutil
import json
import time
import argparse
from pathlib import Path

# how to use the script:
# py .\backup_v2.py -s "C:/Users/Arash/Desktop/Academic" -d "G:/theAcademicBackup"


def get_file_mod_time(path: Path):
    """Return the last modification time as float seconds."""
    return path.stat().st_mtime


def load_backup_metadata(backup_root: Path):
    metadata_file = backup_root / "backup_metadata.json"
    if metadata_file.exists():
        with metadata_file.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_backup_metadata(backup_root: Path, metadata):
    metadata_file = backup_root / "backup_metadata.json"
    with metadata_file.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def safe_copy(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def perform_backup(source_root: str, backup_root: str):
    source_root = Path(source_root)
    backup_root = Path(backup_root)

    metadata = load_backup_metadata(backup_root)
    new_metadata = {}

    # Create backup root if missing
    backup_root.mkdir(parents=True, exist_ok=True)

    # Track all source files
    for file_path in source_root.rglob("*"):
        if file_path.is_file():
            rel_path = file_path.relative_to(source_root)
            dst_path = backup_root / rel_path

            mod_time = get_file_mod_time(file_path)
            new_metadata[str(rel_path)] = mod_time

            # If new file or modified
            if (str(rel_path) not in metadata) or (mod_time > metadata[str(rel_path)]):
                print(f"Copying updated file: {rel_path}")
                safe_copy(file_path, dst_path)

    # Handle deleted files
    deleted_files = set(metadata.keys()) - set(new_metadata.keys())
    if deleted_files:
        deleted_folder = backup_root / "deleted" / time.strftime("%Y%m%d_%H%M%S")
        deleted_folder.mkdir(parents=True, exist_ok=True)
        for rel_path in deleted_files:
            old_file = backup_root / rel_path
            if old_file.exists():
                target = deleted_folder / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                print(f"Moving deleted file: {rel_path}")
                shutil.move(str(old_file), str(target))

    # Save new metadata
    save_backup_metadata(backup_root, new_metadata)
    print("Backup completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Incremental backup tool")

    parser.add_argument(
        "--source", "-s", required=True, help="Path to the source directory"
    )

    parser.add_argument(
        "--destination",
        "-d",
        required=True,
        help="Path to the backup destination directory",
    )

    args = parser.parse_args()

    perform_backup(args.source, args.destination)
