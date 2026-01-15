#!/usr/bin/env python3
import sqlite3

DB = "ids.db"

def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # WAL mode for concurrent writes
    cur.execute("PRAGMA journal_mode=WAL;")

    # Create table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS packets (
        ts    FLOAT,
        src   TEXT,
        dst   TEXT,
        sport INT,
        dport INT,
        proto TEXT,
        flags TEXT
    );
    """)

    # Indexes
    cur.execute("CREATE INDEX IF NOT EXISTS idx_src ON packets(src);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ts ON packets(ts);")

    conn.commit()
    conn.close()
    print("Database initialized: ids.db")

if __name__ == "__main__":
    main()
