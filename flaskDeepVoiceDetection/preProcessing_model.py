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

# 학습된 모델 로드
model = load_model("lstm_model_softmax_best.h5")

# 라벨 인코더 설정
label_encoder = LabelEncoder()
label_encoder.classes_ = np.array(["fake", "real"])  # 학습 시 사용된 클래스 순서


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

    return mfcc_features


def predict_audio(file_path):
    """
    오디오 파일의 레이블 예측 (fake 또는 real)
    Args:
    - file_path (str): 오디오 파일 경로.

    Returns:
    - dict: 예측 확률과 레이블 정보
    """
    try:
        # 전처리
        mfcc_features = preprocess_audio(file_path)
        print(f"MFCC features extracted: {len(mfcc_features)} segments")

        # 모델 입력 크기에 맞게 패딩
        X_input_padded = pad_sequences(
            mfcc_features, padding="post", dtype="float32", value=0.0)
        print(f"Padded input shape: {X_input_padded.shape}")

        # 모델 예측
        y_pred = model.predict(X_input_padded, verbose=0)
        print(f"Model prediction shape: {y_pred.shape}")

        # 클래스 확률 계산
        class_probabilities = np.mean(y_pred, axis=0)  # 각 클래스의 평균 확률
        print(f"Class probabilities: {class_probabilities}")
        y_pred_class = np.argmax(y_pred, axis=1)

        # 다수결 투표로 최종 예측 결정
        predicted_class_index = np.bincount(y_pred_class).argmax()

        # 예측된 레이블
        predicted_label = label_encoder.inverse_transform([predicted_class_index])[0]
        print(f"Predicted label: {predicted_label}")

        return {
            "real": round(class_probabilities[1] * 100, 2),
            "fake": round(class_probabilities[0] * 100, 2),
        }
    except Exception as e:
        print(f"Error in predict_audio: {e}")
        raise