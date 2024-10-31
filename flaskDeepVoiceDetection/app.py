from flask import Flask, request, redirect, render_template
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
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return '파일이 성공적으로 업로드되었습니다!'

if __name__ == '__main__':
    app.run(debug=True)