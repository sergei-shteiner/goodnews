import os
import sqlite3
import time
from pathlib import Path


DEFAULT_TTL_SECONDS = 120
DB_PATH = Path(os.getenv("PRINT_QUEUE_DB", "print_jobs.sqlite3"))


def _connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS print_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                news TEXT NOT NULL,
                created_at REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                printed_at REAL
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_print_jobs_status_created_at
            ON print_jobs (status, created_at)
            """
        )


def enqueue_print_job(news):
    init_db()
    now = time.time()
    with _connect() as connection:
        cursor = connection.execute(
            "INSERT INTO print_jobs (news, created_at, status) VALUES (?, ?, 'pending')",
            (news, now),
        )
        return cursor.lastrowid


def expire_old_jobs(ttl_seconds=DEFAULT_TTL_SECONDS):
    init_db()
    cutoff = time.time() - ttl_seconds
    with _connect() as connection:
        cursor = connection.execute(
            """
            UPDATE print_jobs
            SET status = 'expired'
            WHERE status = 'pending' AND created_at < ?
            """,
            (cutoff,),
        )
        return cursor.rowcount


def get_pending_print_jobs(ttl_seconds=DEFAULT_TTL_SECONDS):
    init_db()
    expire_old_jobs(ttl_seconds)
    cutoff = time.time() - ttl_seconds
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT id, news, created_at
            FROM print_jobs
            WHERE status = 'pending' AND created_at >= ?
            ORDER BY created_at ASC
            """,
            (cutoff,),
        ).fetchall()
    return [dict(row) for row in rows]


def mark_print_job_done(job_id):
    init_db()
    with _connect() as connection:
        cursor = connection.execute(
            """
            UPDATE print_jobs
            SET status = 'printed', printed_at = ?
            WHERE id = ? AND status = 'pending'
            """,
            (time.time(), job_id),
        )
        return cursor.rowcount > 0
