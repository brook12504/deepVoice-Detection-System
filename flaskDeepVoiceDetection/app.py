from flask import Flask, request, redirect, render_template, jsonify
import os

app = Flask(__name__, static_url_path='/templates/assets', static_folder='templates/assets')

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 최대 16MB 파일 제한

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    if file and allowed_file(file.filename):
        file_name = request.form.get('name', file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(file_path)
        return jsonify({"name": file_name, "real": 37.4, "fake": 62.6})
    return jsonify({"error": "Invalid file type"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)