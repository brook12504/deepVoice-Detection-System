import librosa
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder

# 전처리 설정
n_fft = 1024
hop_length = 512
n_mfcc = 40
segment_length = 2  # 2초 단위 분할


def preprocess_audio(file_path):
    """
    오디오를 2초 단위로 분할하고 각 세그먼트의 MFCC를 추출.
    Args:
    - file_path (str): 오디오 파일 경로.

    Returns:
    - List[np.ndarray]: 각 세그먼트의 MFCC (시간 축이 첫 번째).
    """
    # 오디오 파일 로드
    y_audio, sr = librosa.load(file_path, sr=None)
    segment_samples = int(sr * segment_length)

    # 2초 단위로 분할
    segments = [y_audio[i: i + segment_samples]
                for i in range(0, len(y_audio), segment_samples)]

    # 각 세그먼트에서 MFCC 추출
    mfcc_features = [librosa.feature.mfcc(y=segment, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mfcc=n_mfcc).T
                     for segment in segments]

    return mfcc_features, sr


# 오디오 파일 경로
file_path = "uploads/choi.wav"  # 예측할 오디오 파일 경로

# 오디오 전처리
mfcc_features, sr = preprocess_audio(file_path)

# 모델 입력 크기에 맞게 패딩
X_input_padded = pad_sequences(
    mfcc_features, padding="post", dtype="float32", value=0.0)

# 모델 로드
model = load_model("lstm_model_softmax_best.h5")

# 모델 예측
y_pred = model.predict(X_input_padded, verbose=0)

# 클래스 확률 계산
class_probabilities = np.mean(y_pred, axis=0)  # 각 클래스의 평균 확률
y_pred_class = np.argmax(y_pred, axis=1)

# 다수결 투표로 최종 예측 결정
predicted_class_index = np.bincount(y_pred_class).argmax()

# 라벨 인코딩
label_encoder = LabelEncoder()
label_encoder.classes_ = np.array(["fake", "real"])  # 학습 시 사용된 클래스 순서
predicted_label = label_encoder.inverse_transform([predicted_class_index])

# 결과 출력
print(f"Predicted Label: {predicted_label[0]}")
print(
    f"Class Probabilities: {dict(zip(label_encoder.classes_, class_probabilities * 100))}")
