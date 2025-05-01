import sqlite3
import os
from datetime import datetime
from flask import current_app
from config import Config

def get_db():
    config = Config()
    db_path = config.get_db_path()
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Create the documents table with indexes
    c.execute('''
        CREATE TABLE IF NOT EXISTS documents
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         content TEXT NOT NULL,
         creator_name TEXT NOT NULL,
         price REAL NOT NULL,
         date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')
    
    # Add indexes for better query performance
    c.execute('CREATE INDEX IF NOT EXISTS idx_name ON documents(name)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_creator ON documents(creator_name)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_date ON documents(date_created)')
    
    # Add sample data if table is empty
    c.execute('SELECT COUNT(*) FROM documents')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO documents (name, content, creator_name, price)
            VALUES (?, ?, ?, ?)
        ''', (
            'Sample Market Report 2024',
            'This is a sample market report analyzing key trends...',
            'John Smith',
            29.99
        ))
    
    conn.commit()
    conn.close()

class Document:
    @staticmethod
    def get_all():
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id, name, creator_name, price, date_created FROM documents')
        documents = c.fetchall()
        conn.close()
        return documents

    @staticmethod
    def get_by_id(doc_id):
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM documents WHERE id = ?', (doc_id,))
        document = c.fetchone()
        conn.close()
        return document

    @staticmethod
    def create(name, content, creator_name, price):
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO documents (name, content, creator_name, price)
            VALUES (?, ?, ?, ?)
        ''', (name, content, creator_name, price))
        conn.commit()
        doc_id = c.lastrowid
        conn.close()
        return doc_id