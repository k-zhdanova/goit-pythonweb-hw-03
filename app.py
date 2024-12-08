from flask import Flask, render_template, request, redirect, url_for, abort
import json
from datetime import datetime
import os

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'storage'

# Ініціалізація файлу даних
DATA_FILE = os.path.join(app.config['UPLOAD_FOLDER'], 'data.json')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

# Сторінка повідомлень
@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form.get('username')
        message = request.form.get('message')

        if username and message:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)

            timestamp = str(datetime.now())
            data[timestamp] = {'username': username, 'message': message}

            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=4)

            return redirect(url_for('index'))

    return render_template('message.html')

# Читання повідомлень
@app.route('/read')
def read():
    with open(DATA_FILE, 'r') as f:
        messages = json.load(f)
    return render_template('read.html', messages=messages)

# Обробка 404 помилок
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
