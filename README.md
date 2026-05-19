# GSM-Bot: Project Zomboid Server Manager

GSM-Bot is an open-source tool that allows you to launch a dedicated Project Zomboid server using Docker with just one command. It includes an automated background script to handle game saves and backups, ensuring you never lose progress.

## Features

- **One-Click Launch**: Start your server and backup manager with a single command.
- **Automated Backups**: Backs up game data every 5 hours (configurable).
- **Smart Retention**: Automatically keeps backups for 3 days to save disk space.
- **Manual Backups**: Trigger a backup whenever you want.
- **Cloud Integration**: Optional sync to Google Drive or other cloud providers via `rclone`.
- **Easy Restoration**: Simple interactive script to restore from timestamped backups.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Getting Started

### 1. Configuration

Clone this repository and navigate to the directory. Open the `.env` file to configure your server settings:

```bash
# .env file
SERVER_NAME=MyAwesomeServer
SERVER_PASSWORD=secret
ADMIN_PASSWORD=verysecret
MAX_PLAYERS=16

# Backup Settings
BACKUP_INTERVAL_HOURS=5
BACKUP_RETENTION_DAYS=3
```

### 2. Launch the Server

Run the following command to start the server and the backup manager:

```bash
docker compose up -d
```

Your Project Zomboid server will now start pulling the necessary images and initialize.

---

## Usage

### Connecting to the Server

- **IP**: Your server's IP address.
- **Port**: 16261 (UDP)

### Manual Backups

If you want to trigger a backup immediately (e.g., before an update or a risky move), run:

```bash
docker exec pz-backup-manager python backup.py
```

### Restoring a Backup

To restore your server to a previous state:

1.  Run the restore script:
    ```bash
    docker exec -it pz-backup-manager python restore.py
    ```
2.  Follow the interactive prompt to select the backup you want to restore.
3.  **Restart the server** to apply changes:
    ```bash
    docker compose restart zomboid-server
    ```

### Cloud Backups (Optional)

GSM-Bot supports `rclone` for cloud backups.

1.  Configure `rclone` on your host machine or within the container.
2.  Update `.env`:
    ```bash
    ENABLE_CLOUD_BACKUP=true
    RCLONE_REMOTE_NAME=your_remote_name
    ```
3.  Ensure your `rclone.conf` is accessible at `~/.config/rclone/rclone.conf`.

---

## Technical Architecture

- **zomboid-server**: Runs the game using the `pepecitron/projectzomboid-server` image.
- **backup-manager**: A Python-based sidecar container that monitors the `/game-data` volume, compresses it into `/backups`, and handles retention/cloud sync.

## Directory Structure

- `game-data/`: Contains server configuration and save files.
- `backups/`: Local directory where `.zip` backups are stored.
- `scripts/`: Source code for the backup and restore logic.
