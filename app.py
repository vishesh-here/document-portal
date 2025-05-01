from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-123')

# Hardcoded credentials
USER_CREDENTIALS = {
    'user@example.com': 'password123',
    'admin@example.com': 'admin123'
}

DOCUMENT_PASSWORD = '1234'  # Hardcoded document access password

def get_db_path():
    # Use /var/data directory for persistent storage on Render
    if os.environ.get('RENDER'):
        os.makedirs('/var/data', exist_ok=True)
        return '/var/data/documents.db'
    return 'documents.db'

def init_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
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
    
    # Add some initial sample data if table is empty
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

def setup():
    init_db()

# Initialize the database when the app starts
with app.app_context():
    setup()

@app.route('/')
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('documents'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in USER_CREDENTIALS and USER_CREDENTIALS[email] == password:
            session['email'] = email
            session['is_admin'] = (email == 'admin@example.com')
            return redirect(url_for('documents'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/documents')
def documents():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, name, creator_name, price, date_created FROM documents')
    documents = c.fetchall()
    conn.close()
    
    return render_template('documents.html', 
                         documents=documents,
                         is_admin=session.get('is_admin', False))

@app.route('/document/<int:doc_id>')
def get_document(doc_id):
    if 'email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM documents WHERE id = ?', (doc_id,))
    document = c.fetchone()
    conn.close()
    
    if not document:
        return jsonify({'error': 'Document not found'}), 404
        
    return jsonify({
        'id': document[0],
        'name': document[1],
        'content': document[2],
        'creator_name': document[3],
        'price': document[4],
        'date_created': document[5]
    })

@app.route('/verify-password', methods=['POST'])
def verify_password():
    password = request.json.get('password')
    if password == DOCUMENT_PASSWORD:
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/admin/upload', methods=['POST'])
def upload_document():
    if 'email' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    name = request.form.get('name')
    content = request.form.get('content')
    creator_name = request.form.get('creator_name')
    price = request.form.get('price')
    
    if not all([name, content, creator_name, price]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO documents (name, content, creator_name, price)
        VALUES (?, ?, ?, ?)
    ''', (name, content, creator_name, price))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)