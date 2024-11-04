from flask import Flask, request, redirect, render_template, jsonify
import os

app = Flask(__name__, static_url_path='/templates/assets', static_folder='templates/assets')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# uploads 폴더가 없으면 생성합니다.
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
    # 요청에서 파일과 파일명을 받습니다.
    if 'audioFile' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['audioFile']
    file_name = request.form.get('name', file.filename)  # 파일명이 없으면 파일 이름으로 대체

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # 파일 저장 경로를 설정합니다.
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(file_path)  # 파일 저장

        # 응답을 JSON 형식으로 반환합니다.
        return jsonify({"name": file_name, "real": 12, "fake": 88})

if __name__ == '__main__':
    app.run(debug=True)