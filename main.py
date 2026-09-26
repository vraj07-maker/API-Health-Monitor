from fastapi import FastAPI, Query
import httpx
import sqlite3
from datetime import datetime

app = FastAPI(title="API Health Monitor")

DB_NAME = "logs.db"

# Initialize database schema safely
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                status_code INTEGER,
                is_online BOOLEAN,
                latency_ms REAL,
                timestamp TEXT
            )
        """)
        conn.commit()

# Run database setup on server start
init_db()

@app.get("/")
def home():
    return {"status": "Monitor active"}

# Asynchronous route handling dynamic URLs
@app.get("/check")
async def check_status(url: str = Query(..., description="Target URL to check")):
    start_time = datetime.now()
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            status_code = response.status_code
            is_online = (200 <= status_code < 400)
    except Exception:
        status_code = 0
        is_online = False

    latency_ms = (datetime.now() - start_time).total_seconds() * 1000
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save check result to database using context manager
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO health_logs (url, status_code, is_online, latency_ms, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (url, status_code, is_online, latency_ms, now))
        conn.commit()

    return {
        "url": url,
        "status_code": status_code,
        "online": is_online,
        "latency_ms": round(latency_ms, 2),
        "logged_at": now
    }

@app.get("/logs")
def get_logs():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM health_logs ORDER BY id DESC LIMIT 50")
        rows = cursor.fetchall()

    return {"total_logs": len(rows), "logs": rows}