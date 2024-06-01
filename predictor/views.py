from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.callbacks import LambdaCallback

# 대회별 최대, 최소값 설정
aptitude_test_max_min = {
    '중대한 사회 안전 이니까': (48, 12),
    '부산 도시브랜드 굿즈 디자인 공모전': (64, 16),
    '인천건축학생공모전': (68, 17),
    'GCGF 혁신 아이디어 공모': (40, 10),
    '웹 개발 콘테스트': (64, 16)
}

# 모델과 스케일러를 전역 변수로 설정하여 재사용
model = None
scaler = None

def load_and_train_model():
    global model, scaler
    
    # 데이터 로드
    df = pd.read_excel('jongsulData.xlsx')
    
    # 특성과 라벨 분리
    X = df.drop(columns=aptitude_test_max_min.keys())
    y = df[list(aptitude_test_max_min.keys())]

    # 학습 데이터와 테스트 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 데이터 정규화
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 모델 구성
    model = tf.keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[X_train_scaled.shape[1]]),
        layers.Dense(64, activation='relu'),
        layers.Dense(5)  # 출력층
    ])

    # 모델 컴파일
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    # 콜백 함수 설정
    print_callback = LambdaCallback(on_epoch_end=lambda epoch, logs: print(f"Epoch {epoch + 1}: loss = {logs['loss']}, mae = {logs['mae']}"))

    # 모델 학습
    model.fit(X_train_scaled, y_train, epochs=50, validation_split=0.2, callbacks=[print_callback])

    # 모델 평가
    mse, mae = model.evaluate(X_test_scaled, y_test)
    print(f"Test MSE: {mse}")
    print(f"Test MAE: {mae}")

@csrf_exempt
def predict_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # 요청 데이터 처리
        students = data.get('students')
        if not students:
            return JsonResponse({'error': 'No student data provided'}, status=400)

        predictions = []
        for student in students:
            new_student_data = {
                'grade': student.get('grade'),
                'depart': student.get('depart'),
                'credit': student.get('credit'),
                'in_school_award_cnt': student.get('in_school_award_cnt'),
                'out_school_award_cnt': student.get('out_school_award_cnt'),
                'national_competition_award_cnt': student.get('national_competition_award_cnt'),
                'aptitude_test_score': student.get('aptitude_test_score'),
                'certificate': student.get('certificate'),
                'major_field': student.get('major_field'),
                'codingTest_score': student.get('codingTest_score')
            }

            try:
                # 모델 예측 함수 호출
                prediction = predict_contest_winning_probabilities(new_student_data)
                predictions.append(prediction)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        
        return JsonResponse({'predictions': predictions})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def predict_contest_winning_probabilities(new_student_data):
    # 데이터 프레임 생성
    new_student_df = pd.DataFrame([new_student_data])
    
    # NaN 값 확인 및 처리
    if new_student_df.isnull().values.any():
        raise ValueError("Input data contains NaN values")
    
    # 데이터 타입 변환
    new_student_df = new_student_df.astype(float)
    
    # 데이터 스케일링
    if scaler is None:
        raise ValueError("Scaler is not initialized")
    new_student_data_scaled = scaler.transform(new_student_df)
    
    # 예측
    if model is None:
        raise ValueError("Model is not initialized")
    predictions = model.predict(new_student_data_scaled)[0]
    
    # 확률값을 0과 100 사이의 값으로 변환
    predictions = np.clip(predictions, 0, 100)
    
    # float32 값을 float으로 변환
    predictions = predictions.astype(float)
    
    return {contest: float(prob) for contest, prob in zip(aptitude_test_max_min.keys(), predictions)}


load_and_train_model()
