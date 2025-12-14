import os
import logging
import sqlite3
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
app = Flask(__name__)

# --- Paths ---
DATA_DIR = os.environ.get('DATA_DIR', 'data')
UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
DB_FILE = os.path.join(DATA_DIR, 'shuttle.db')

# Ensure directories exist
for folder in [DATA_DIR, UPLOAD_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# --- Database Management ---
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def init_db():
    conn = get_db_connection()
    # Table stores text content AND/OR filename
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pastes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            filename TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        filename = None
        
        # Handle File Upload
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        # Only save if there is content or a file
        if content or filename:
            conn.execute('INSERT INTO pastes (content, filename) VALUES (?, ?)', 
                         (content, filename))
            conn.commit()
            
        conn.close()
        return redirect(url_for('index'))

    # GET: Fetch all pastes, newest first
    pastes = conn.execute('SELECT * FROM pastes ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', pastes=pastes)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_paste(id):
    conn = get_db_connection()
    
    # Optional: Delete the actual file from disk if you want to save space
    paste = conn.execute('SELECT filename FROM pastes WHERE id = ?', (id,)).fetchone()
    if paste and paste['filename']:
        file_path = os.path.join(UPLOAD_FOLDER, paste['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)

    conn.execute('DELETE FROM pastes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)