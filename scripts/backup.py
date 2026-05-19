import os
import time
import zipfile
import shutil
from datetime import datetime
import subprocess

# Configuration from environment variables
BACKUP_INTERVAL_HOURS = int(os.environ.get('BACKUP_INTERVAL_HOURS', 5))
BACKUP_RETENTION_DAYS = int(os.environ.get('BACKUP_RETENTION_DAYS', 3))
GAME_DATA_PATH = os.environ.get('GAME_DATA_PATH', '/game-data')
BACKUP_PATH = os.environ.get('BACKUP_PATH', '/backups')
ENABLE_CLOUD_BACKUP = os.environ.get('ENABLE_CLOUD_BACKUP', 'false').lower() == 'true'
RCLONE_REMOTE_NAME = os.environ.get('RCLONE_REMOTE_NAME', 'gdrive')

def create_backup():
    print(f"[{datetime.now()}] Starting backup...")

    # Ensure backup directory exists
    if not os.path.exists(BACKUP_PATH):
        os.makedirs(BACKUP_PATH)

    # Timestamp for the backup
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_filename = f"backup-{timestamp}.zip"
    backup_file_path = os.path.join(BACKUP_PATH, backup_filename)

    try:
        # Create zip file
        with zipfile.ZipFile(backup_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(GAME_DATA_PATH):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Relative path for the zip file
                    arcname = os.path.relpath(file_path, GAME_DATA_PATH)
                    zipf.write(file_path, arcname)

        print(f"[{datetime.now()}] Backup created successfully: {backup_filename}")

        # Cloud backup if enabled
        if ENABLE_CLOUD_BACKUP:
            upload_to_cloud(backup_file_path)

        # Cleanup old backups
        cleanup_old_backups()

    except Exception as e:
        print(f"[{datetime.now()}] Error during backup: {e}")

def upload_to_cloud(file_path):
    print(f"[{datetime.now()}] Uploading to cloud via rclone...")
    try:
        # rclone copy <file> <remote>:<path>
        cmd = ["rclone", "copy", file_path, f"{RCLONE_REMOTE_NAME}:GSM-Backups/"]
        subprocess.run(cmd, check=True)
        print(f"[{datetime.now()}] Cloud upload successful.")
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now()}] Cloud upload failed: {e}")

def cleanup_old_backups():
    print(f"[{datetime.now()}] Cleaning up backups older than {BACKUP_RETENTION_DAYS} days...")
    now = time.time()
    retention_seconds = BACKUP_RETENTION_DAYS * 24 * 60 * 60

    for filename in os.listdir(BACKUP_PATH):
        if filename.startswith("backup-") and filename.endswith(".zip"):
            file_path = os.path.join(BACKUP_PATH, filename)
            if os.path.getmtime(file_path) < now - retention_seconds:
                try:
                    os.remove(file_path)
                    print(f"[{datetime.now()}] Deleted old backup: {filename}")
                except Exception as e:
                    print(f"[{datetime.now()}] Failed to delete {filename}: {e}")

def run_scheduler():
    interval_seconds = BACKUP_INTERVAL_HOURS * 3600
    print(f"[{datetime.now()}] Backup manager started. Interval: {BACKUP_INTERVAL_HOURS} hours.")

    # Run first backup immediately on startup
    create_backup()

    while True:
        time.sleep(interval_seconds)
        create_backup()

if __name__ == "__main__":
    run_scheduler()
