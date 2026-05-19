# GSM-Bot: Universal Game Server Manager

GSM-Bot is an open-source tool that allows you to launch **any** dedicated game server using Docker with just one command. It includes a professional web-based dashboard and automated background backups.

## Features

- **Professional GUI**: Modern, dark-themed dashboard to manage your server.
- **Universal Compatibility**: Works with any game that has a Docker image (Minecraft, Project Zomboid, Valheim, etc.).
- **One-Click Launch**: Use `./start.sh` to launch the server and open the dashboard automatically.
- **Automated Backups**: Backs up game data every 5 hours (configurable).
- **Easy Restoration**: Restore from timestamped backups directly via the GUI.
- **Cloud Integration**: Optional sync to Google Drive via `rclone`.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Quick Start

1.  **Launch Everything**:
    ```bash
    chmod +x start.sh
    ./start.sh
    ```
    This will start the server and automatically open the dashboard at `http://localhost:3000`.

2.  **Login**: Use the default password `admin` (or leave it blank if not configured).

---

## Configuration

### Core Settings (`.env`)
Configure the core infrastructure and backup settings here.

### Game Settings (`game.env`)
Add game-specific environment variables (e.g., `SERVER_PASSWORD`, `EULA=TRUE`).

**Note**: You can also edit these directly in the **Settings** tab of the GUI!

---

## Usage

### Dashboard
- **Console**: View live server logs.
- **Controls**: Start, Stop, or Restart your server instance.
- **Manual Backup**: Click "Backup Now" (with confirmation) to trigger an immediate save.

### Backups
- View all historical backups.
- Click **Restore** to roll back your server to a specific point in time.

---

## Technical Architecture

- **gsm-gui**: Static frontend (Nginx) at port 3000.
- **gsm-backend**: FastAPI server at port 8000 (controls Docker).
- **game-server**: Your chosen game container.
- **backup-manager**: Sidecar container for automated tasks.

## Directory Structure
- `game-data/`: Shared volume for game saves/config.
- `backups/`: Local storage for `.zip` files.
- `gui/`: Source code for the dashboard.
