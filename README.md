# GSM-Bot: Universal Game Server Manager

GSM-Bot is an open-source tool that allows you to launch **any** dedicated game server using Docker with just one command. It includes an automated background script to handle game saves and backups, ensuring you never lose progress.

## Features

- **Universal Compatibility**: Works with any game that has a Docker image (Minecraft, Project Zomboid, Valheim, etc.).
- **One-Click Launch**: Start your server and backup manager with a single command.
- **Automated Backups**: Backs up game data every 5 hours (configurable).
- **Smart Retention**: Automatically keeps backups for 3 days to save disk space.
- **Cloud Integration**: Optional sync to Google Drive or other cloud providers via `rclone`.
- **Easy Restoration**: Simple interactive script to restore from timestamped backups.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Getting Started

### 1. Basic Configuration (`.env`)

Configure the core settings in the `.env` file:

```bash
# Game Image (e.g., itzg/minecraft-server or pepecitron/projectzomboid-server)
GAME_IMAGE=pepecitron/projectzomboid-server

# Internal path where the game stores saves
GAME_INTERNAL_DATA_PATH=/data

# Ports to expose (host:container/protocol)
GAME_PORT_1=16261:16261/udp
GAME_PORT_2=16262:16262/udp

# Backup Settings
BACKUP_INTERVAL_HOURS=5
BACKUP_RETENTION_DAYS=3
```

### 2. Game-Specific Configuration (`game.env`)

Add any environment variables required by your chosen game image to `game.env`.

**Example for Project Zomboid:**
```bash
SERVER_NAME=GSMServer
SERVER_PASSWORD=password
SERVER_ADMIN_PASSWORD=adminpassword
```

**Example for Minecraft:**
```bash
EULA=TRUE
MEMORY=4G
```

### 3. Launch the Server

```bash
docker compose up -d
```

---

## Usage

### Manual Backups
Trigger a backup immediately:
```bash
docker exec gsm-backup-manager python backup.py
```

### Restoring a Backup
1. Run the restore script:
   ```bash
   docker exec -it gsm-backup-manager python restore.py
   ```
2. Follow the prompt and then restart the server:
   ```bash
   docker compose restart game-server
   ```

### Cloud Backups
Update `.env`:
```bash
ENABLE_CLOUD_BACKUP=true
RCLONE_REMOTE_NAME=your_remote
```
Ensure your `rclone.conf` is at `~/.config/rclone/rclone.conf`.

---

## Technical Architecture

GSM-Bot uses a sidecar pattern:
- **game-server**: The container running your game.
- **backup-manager**: A Python-based container that monitors `./game-data` and manages backups.

## Directory Structure
- `game-data/`: Local folder mapped to the game's internal data path.
- `backups/`: Local storage for `.zip` backups.
- `scripts/`: Backup and restore logic.
