import os
import zipfile
import shutil
from datetime import datetime

BACKUP_PATH = os.environ.get('BACKUP_PATH', '/backups')
GAME_DATA_PATH = os.environ.get('GAME_DATA_PATH', '/game-data')

def list_backups():
    backups = [f for f in os.listdir(BACKUP_PATH) if f.startswith('backup-') and f.endswith('.zip')]
    backups.sort(reverse=True)
    return backups

def restore_backup(backup_filename):
    backup_file_path = os.path.join(BACKUP_PATH, backup_filename)

    if not os.path.exists(backup_file_path):
        print(f"Error: Backup file {backup_filename} not found.")
        return

    print(f"[{datetime.now()}] Starting restoration of {backup_filename}...")

    # Confirm with user if running interactively?
    # Since this is intended to be run via docker exec, we'll just proceed or assume it was intentional.

    try:
        # 1. Clear current game data (optional but recommended for clean restore)
        # We only clear what we are about to restore.
        # PZ server might have files in /game-data/config and /game-data/server-files
        # Our backup contains relative paths from /game-data

        print(f"Cleaning up {GAME_DATA_PATH} before restore...")
        for item in os.listdir(GAME_DATA_PATH):
            item_path = os.path.join(GAME_DATA_PATH, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

        # 2. Extract backup
        with zipfile.ZipFile(backup_file_path, 'r') as zipf:
            zipf.extractall(GAME_DATA_PATH)

        print(f"[{datetime.now()}] Restoration successful!")
        print("NOTE: You MUST restart the zomboid-server container for changes to take effect.")
        print("Command: docker compose restart zomboid-server")

    except Exception as e:
        print(f"[{datetime.now()}] Error during restoration: {e}")

if __name__ == "__main__":
    backups = list_backups()
    if not backups:
        print("No backups found in /backups")
    else:
        print("Available backups:")
        for i, b in enumerate(backups):
            print(f"{i}: {b}")

        choice = input("Enter the number of the backup to restore, or 'q' to quit: ")
        if choice.lower() == 'q':
            exit()

        try:
            index = int(choice)
            if 0 <= index < len(backups):
                restore_backup(backups[index])
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
