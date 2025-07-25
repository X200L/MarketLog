from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
import os
from yanlog import thicken_and_color_image, ImageProcessor
import sqlite3
import hashlib
from main2 import starter

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_1234567890'  
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TEMP_UPLOAD_FOLDER'] = 'temp_uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMP_UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join('backend', 'heatmaps'), exist_ok=True)


# Инициализация базы данных при запуске
if not os.path.exists('database.db'):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/lc')
def lc():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user_dir = os.path.join('user_data', username)
    temp_uploads = os.path.join(user_dir, 'temp_uploads')
    heatmaps = os.path.join(user_dir, 'heatmaps')
    images = []
    heatmap_images = []
    for i in range(6):
        img_path = f'/user_data/{username}/temp_uploads/warehouse_roads{i}.png'
        heatmap_path = f'/user_data/{username}/heatmaps/heatmap{i}.png'
        if os.path.exists(os.path.join(temp_uploads, f'warehouse_roads{i}.png')):
            images.append(img_path)
        else:
            images.append(None)
        if os.path.exists(os.path.join(heatmaps, f'heatmap{i}.png')):
            heatmap_images.append(heatmap_path)
        else:
            heatmap_images.append('')
    return render_template('lc.html', images=images, heatmaps=heatmap_images)


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'user_id' not in session or 'username' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        username = session['username']
        user_dir = os.path.join('user_data', username)
        upload_folder = os.path.join(user_dir, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        file.save(os.path.join(upload_folder, file.filename))
        return jsonify({'message': 'File uploaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/file')
def file_page():
    return render_template('file.html')


@app.route('/build-grid', methods=['POST'])
def build_grid():
    try:
        if 'user_id' not in session or 'username' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        username = session['username']
        user_dir = os.path.join('user_data', username)
        upload_folder = os.path.join(user_dir, 'uploads')
        temp_upload_folder = os.path.join(user_dir, 'temp_uploads')
        heatmaps_folder = os.path.join(user_dir, 'heatmaps')
        graph_folder = os.path.join(user_dir, 'graph')
        data = request.get_json()
        if not data or 'filename' not in data:
            return jsonify({'error': 'No filename provided'}), 400
        filename = data['filename']
        operation_zone_x = int(data.get('operation_zone_x', 350))
        operation_zone_y = int(data.get('operation_zone_y', 150))
        robot_size = int(data.get('robot_size', 30))
        image_path = os.path.join(upload_folder, filename)
        processor = ImageProcessor(upload_folder)
        processed_filename = processor.process_file(filename)
        processed_path = os.path.join(upload_folder, processed_filename)
        starter(processed_path, operation_zone_x, operation_zone_y, robot_size, temp_upload_folder=temp_upload_folder, user_dir=user_dir)
        images = [f'/user_data/{username}/temp_uploads/warehouse_roads{i}.png' for i in range(6)]
        heatmaps = [f'/user_data/{username}/heatmaps/heatmap{i}.png' for i in range(6)]
        return jsonify({
            'message': 'Grid built successfully',
            'images': images,
            'heatmaps': heatmaps
        })
    except FileNotFoundError as e:
        return jsonify({'error': f'File not found: {str(e)}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'temp_uploads'))
    return send_from_directory(abs_path, filename)

@app.route('/temp_uploads/<filename>')
def temp_uploaded_file(filename):
    # Абсолютный путь к папке temp_uploads относительно корня проекта
    project_root = os.path.abspath(os.path.dirname(__file__) + '/../')
    abs_path = os.path.join(project_root, 'temp_uploads')
    return send_from_directory(abs_path, filename)

@app.route('/heatmaps/<filename>')
def heatmap_file(filename):
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'heatmaps'))
    return send_from_directory(abs_path, filename)

@app.route('/user_data/<username>/<folder>/<filename>')
def user_file(username, folder, filename):
    abs_path = os.path.abspath(os.path.join('user_data', username, folder))
    return send_from_directory(abs_path, filename)


def create_user(username, password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()
    # Создание пользовательских папок
    user_dir = os.path.join('user_data', username)
    os.makedirs(os.path.join(user_dir, 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(user_dir, 'temp_uploads'), exist_ok=True)
    os.makedirs(os.path.join(user_dir, 'heatmaps'), exist_ok=True)
    os.makedirs(os.path.join(user_dir, 'graph'), exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        if password != password2:
            error = 'Пароли не совпадают'
        elif not username or not password:
            error = 'Заполните все поля'
        else:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            if user:
                error = 'Пользователь уже существует'
            else:
                create_user(username, password)
                conn.close()
                return redirect(url_for('login'))
            conn.close()
    return render_template('reg.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            error = 'Заполните все поля'
        else:
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            conn.close()
            if user and user['password'] == hashed_password:
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('lc'))
            else:
                error = 'Неправильное имя пользователя или пароль'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)