import sqlite3
import os
from flask import g

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'vix_ninja.sqlite')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE_PATH,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    # Create tables
    db.execute('''
    CREATE TABLE IF NOT EXISTS vix_futures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME NOT NULL,
        contract_month TEXT NOT NULL,
        price REAL NOT NULL,
        open_interest INTEGER,
        volume INTEGER,
        UNIQUE(timestamp, contract_month)
    )
    ''')
    
    db.execute('''
    CREATE TABLE IF NOT EXISTS vix_index (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME NOT NULL,
        value REAL NOT NULL,
        UNIQUE(timestamp)
    )
    ''')
    
    db.commit()

# Call init_db to ensure tables exist
init_db()