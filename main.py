from fastapi import FastAPI
import requests
import sqlite3
from datetime import datetime

app = FastAPI()

# Function to initialize the database and create our logs table
def init_db():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            status_code INTEGER,
            is_online BOOLEAN,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# Run database creation on startup
init_db()

@app.get("/")
def home():
    return {"status": "Monitor active"}

@app.get("/check")
def check_status():
    target_url = "https://httpbin.org/status/200"
    response = requests.get(target_url)
    
    status_code = response.status_code
    is_online = (status_code == 200)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save check result directly into SQL
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO health_logs (url, status_code, is_online, timestamp)
        VALUES (?, ?, ?, ?)
    """, (target_url, status_code, is_online, now))
    conn.commit()
    conn.close()

    return {
        "url": target_url,
        "status_code": status_code,
        "online": is_online,
        "logged_at": now
    }

# New Endpoint: View all logged health checks from the SQL database
@app.get("/logs")
def get_logs():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health_logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    return {"total_logs": len(rows), "logs": rows}