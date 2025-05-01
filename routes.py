from flask import render_template, request, jsonify, session, redirect, url_for, flash
from functools import wraps
from models import Document
from config import USER_CREDENTIALS, Config

def init_routes(app):
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'email' not in session:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    def admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'email' not in session or not session.get('is_admin'):
                return jsonify({'error': 'Unauthorized'}), 401
            return f(*args, **kwargs)
        return decorated_function

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
                flash('Successfully logged in!', 'success')
                return redirect(url_for('documents'))
            
            return render_template('login.html', error='Invalid credentials')
        
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Successfully logged out!', 'success')
        return redirect(url_for('login'))

    @app.route('/documents')
    @login_required
    def documents():
        documents = Document.get_all()
        return render_template('documents.html', 
                             documents=documents,
                             is_admin=session.get('is_admin', False))

    @app.route('/document/<int:doc_id>')
    @login_required
    def get_document(doc_id):
        document = Document.get_by_id(doc_id)
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
            
        return jsonify({
            'id': document['id'],
            'name': document['name'],
            'content': document['content'],
            'creator_name': document['creator_name'],
            'price': document['price'],
            'date_created': document['date_created']
        })

    @app.route('/verify-password', methods=['POST'])
    @login_required
    def verify_password():
        password = request.json.get('password')
        config = Config()
        if password == config.DOCUMENT_PASSWORD:
            return jsonify({'success': True})
        return jsonify({'success': False})

    @app.route('/admin/upload', methods=['POST'])
    @admin_required
    def upload_document():
        name = request.form.get('name')
        content = request.form.get('content')
        creator_name = request.form.get('creator_name')
        price = request.form.get('price')
        
        if not all([name, content, creator_name, price]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        try:
            price = float(price)
            Document.create(name, content, creator_name, price)
            return jsonify({'success': True})
        except ValueError:
            return jsonify({'error': 'Invalid price format'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500