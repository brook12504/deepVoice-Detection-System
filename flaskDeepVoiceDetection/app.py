from doctest import debug

from flask import Flask, request, redirect, render_template, jsonify
import os
import threading
import time
from pydub import AudioSegment
from preProcessing_model import predict_audio  # Import 추가



app = Flask(__name__, static_url_path='/templates/assets', static_folder='templates/assets')

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 최대 16MB 파일 제한

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a'}

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
        print(f"File saved at: {file_path}")

        # 파일 확장자 확인
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            return jsonify({"error": "Unsupported file type"}), 400

        # WAV 파일로 변환
        try:
            print(f"Checking FFmpeg path: {AudioSegment.converter}")
            print(f"Checking ffprobe path: {AudioSegment.ffprobe}")
            print(f"System PATH: {os.getenv('PATH')}")
            wav_file_path = os.path.splitext(file_path)[0] + ".wav"
            if file_ext != 'wav':  # 이미 WAV 파일이 아닌 경우 변환
                print(f"Converting file to WAV format: {file_ext}")
                audio = AudioSegment.from_file(file_path, format=file_ext)
                audio.export(wav_file_path, format="wav")
                os.remove(file_path)  # 원본 파일 삭제
                print(f"Converted file to WAV: {wav_file_path}")
            else:
                wav_file_path = file_path  # WAV 파일은 그대로 사용

            # 파일 예측
            print(f"Starting prediction for: {wav_file_path}")
            prediction = predict_audio(wav_file_path)
            print(f"Prediction completed: {prediction}")

            # NumPy 타입을 Python 기본 타입으로 변환
            prediction["real"] = float(prediction["real"])
            prediction["fake"] = float(prediction["fake"])

            # 백그라운드에서 일정 시간 후 파일 삭제
            threading.Thread(target=delete_file_later, args=(wav_file_path, 600)).start()
            # 파일 처리 (예: 예측 작업)


            return jsonify({
                "name": file_name,
                "real": prediction["real"],
                "fake": prediction["fake"]
            })


        except Exception as e:
            print(f"Error during processing: {e}")
            return jsonify({"error": f"File processing failed: {str(e)}"}), 500


if __name__ == "__main__":
    # 현재 파일(app.py)의 디렉토리를 기준으로 FFmpeg 경로 설정
    ffmpeg_path = "/app/ffmpeg-7.1-full_build/bin"

    os.environ["PATH"] += os.pathsep + ffmpeg_path  # PATH에 FFmpeg 경로 추가
    AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg")  # FFmpeg 실행 파일 경로
    AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe")  # ffprobe 실행 파일 경로
    app.run(host="0.0.0.0", port=5000)