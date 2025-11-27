# app/database.py
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "results", "output.db")

def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

_conn = get_conn()

def init_db():
    cur = _conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        jd TEXT
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id INTEGER,
        filename TEXT,
        sim_score REAL,
        keyword_score REAL,
        combined_score REAL,
        matched_keywords TEXT,
        missing_keywords TEXT,
        FOREIGN KEY(run_id) REFERENCES runs(id)
    );
    """)
    _conn.commit()

def create_run(jd_text: str) -> int:
    ts = datetime.utcnow().isoformat()
    cur = _conn.cursor()
    cur.execute("INSERT INTO runs (timestamp, jd) VALUES (?, ?)", (ts, jd_text))
    _conn.commit()
    return cur.lastrowid

def save_candidate(run_id: int, filename: str, sim_score: float, keyword_score: float, combined_score: float,
                   matched_keywords: list, missing_keywords: list):
    cur = _conn.cursor()
    cur.execute("""
        INSERT INTO candidates (run_id, filename, sim_score, keyword_score, combined_score, matched_keywords, missing_keywords)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (run_id, filename, sim_score, keyword_score, combined_score,
          ";".join(matched_keywords), ";".join(missing_keywords)))
    _conn.commit()

def get_runs(limit: int = 20) -> List[Dict[str, Any]]:
    cur = _conn.cursor()
    cur.execute("SELECT id, timestamp FROM runs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    return [dict(r) for r in rows]

def get_candidates_for_run(run_id: int) -> List[Dict[str, Any]]:
    cur = _conn.cursor()
    cur.execute("SELECT filename, sim_score, keyword_score, combined_score, matched_keywords, missing_keywords FROM candidates WHERE run_id = ? ORDER BY combined_score DESC", (run_id,))
    rows = cur.fetchall()
    return [dict(r) for r in rows]

# Initialize DB when imported
init_db()
