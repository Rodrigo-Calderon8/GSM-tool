from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import docker
import os
import subprocess
from pydantic import BaseModel
from typing import List, Optional
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = docker.from_env()

# Paths
ENV_PATH = "/app/.env"
GAME_ENV_PATH = "/app/game.env"
BACKUP_PATH = "/backups"

class ServerStatus(BaseModel):
    status: str
    image: str
    ports: dict

class BackupInfo(BaseModel):
    filename: str
    size: str
    date: str

class Settings(BaseModel):
    env: dict
    game_env: dict

@app.get("/api/status")
async def get_status():
    try:
        container = client.containers.get("gsm-game-server")
        return {
            "status": container.status,
            "image": container.image.tags[0] if container.image.tags else "unknown",
            "ports": container.ports
        }
    except docker.errors.NotFound:
        return {"status": "not_found", "image": "N/A", "ports": {}}

@app.post("/api/server/{action}")
async def server_action(action: str):
    try:
        container = client.containers.get("gsm-game-server")
        if action == "start":
            container.start()
        elif action == "stop":
            container.stop()
        elif action == "restart":
            container.restart()
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
        return {"message": f"Server {action}ed"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Server container not found")

@app.get("/api/logs")
async def get_logs():
    try:
        container = client.containers.get("gsm-game-server")
        logs = container.logs(tail=100).decode("utf-8")
        return {"logs": logs}
    except docker.errors.NotFound:
        return {"logs": "Server not running."}

@app.get("/api/backups", response_model=List[BackupInfo])
async def list_backups():
    if not os.path.exists(BACKUP_PATH):
        return []

    backups = []
    for f in os.listdir(BACKUP_PATH):
        if f.endswith(".zip"):
            path = os.path.join(BACKUP_PATH, f)
            stat = os.stat(path)
            backups.append(BackupInfo(
                filename=f,
                size=f"{stat.st_size / (1024*1024):.2f} MB",
                date=time.ctime(stat.st_mtime)
            ))
    backups.sort(key=lambda x: x.date, reverse=True)
    return backups

@app.post("/api/backup/now")
async def trigger_backup():
    try:
        # Trigger the backup script in the backup-manager container
        container = client.containers.get("gsm-backup-manager")
        result = container.exec_run("python backup.py")
        return {"message": "Backup triggered", "output": result.output.decode("utf-8")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/settings", response_model=Settings)
async def get_settings():
    def parse_env(path):
        env = {}
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        env[key] = value
        return env

    return Settings(
        env=parse_env(ENV_PATH),
        game_env=parse_env(GAME_ENV_PATH)
    )

@app.post("/api/settings")
async def update_settings(settings: Settings):
    def save_env(path, data):
        with open(path, "w") as f:
            for key, value in data.items():
                f.write(f"{key}={value}\n")

    save_env(ENV_PATH, settings.env)
    save_env(GAME_ENV_PATH, settings.game_env)
    return {"message": "Settings updated. Restart may be required."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
