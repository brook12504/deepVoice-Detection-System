from doctest import debug

from flask import Flask, request, redirect, render_template, jsonify
import os
import threading
import time


app = Flask(__name__, static_url_path='/templates/assets', static_folder='templates/assets')

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 최대 16MB 파일 제한

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 일정 시간 후 파일 삭제 함수
def delete_file_later(file_path, delay=300):  # delay는 초 단위 (기본 5분)
    time.sleep(delay)
    if os.path.exists(file_path):
        os.remove(file_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/input-page')
def input_page():
    return render_template('input-page.html')

@app.route('/output-page')
def output_page():
    return render_template('output-page.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audioFile' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['audioFile']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_name = request.form.get('name', file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(file_path)

        # 파일 처리 (예: 예측 작업)
        response_data = {"name": file_name, "real": 37.4, "fake": 62.6}

        # 백그라운드에서 일정 시간 후 파일 삭제
        threading.Thread(target=delete_file_later, args=(file_path, 600)).start()

        return jsonify(response_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000 , debug=True)