import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# 대회별 최대, 최소값 설정
aptitude_test_max_min = {
    '중대한 사회 안전 이니까': (48, 12),
    '부산 도시브랜드 굿즈 디자인 공모전': (64, 16),
    '인천건축학생공모전': (68, 17),
    'GCGF 혁신 아이디어 공모': (40, 10),
    '웹 개발 콘테스트': (64, 16)
}

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
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[X_train_scaled.shape[1]]),
    layers.Dense(64, activation='relu'),
    layers.Dense(5)  # 출력층
])

# 모델 컴파일
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 모델 학습
history = model.fit(X_train_scaled, y_train, epochs=50, validation_split=0.2)

# 모델 평가
mse, mae = model.evaluate(X_test_scaled, y_test)
print("평균 제곱 오차:", mse)
print("평균 절대 오차:", mae)

# 새로운 학생 데이터 예측
def predict_contest_winning_probabilities(new_student_data):
    new_student_df = pd.DataFrame([new_student_data], columns=X.columns)
    new_student_data_scaled = scaler.transform(new_student_df)
    predictions = model.predict(new_student_data_scaled)[0]
    
    # 확률값을 0과 100 사이의 값으로 변환
    predictions = np.clip(predictions, 0, 100)

    
    
    return {contest: prob for contest, prob in zip(aptitude_test_max_min.keys(), predictions)}

# 여러 학생 데이터 생성
student_data_list = [
    {
        'grade': 3,
        'depart': 2,
        'credit': 2,
        'in_school_award_cnt': 1,
        'out_school_award_cnt': 1,
        'national_competition_award_cnt': 2,
        'aptitude_test_score': 50,
        'certificate': 10,
        'major_field': 10,
        'codingTest_score': 2
    },
    {
        'grade': 4,
        'depart': 3,
        'credit': 4.5,
        'in_school_award_cnt': 5,
        'out_school_award_cnt': 5,
        'national_competition_award_cnt': 3,
        'aptitude_test_score': 62,
        'certificate': 12,
        'major_field': 13,
        'codingTest_score': 2
    },
    # 더 많은 학생 데이터 추가 가능
    {
        'grade': 1,
        'depart': 1,
        'credit': 1,
        'in_school_award_cnt': 0,
        'out_school_award_cnt': 2,
        'national_competition_award_cnt': 0,
        'aptitude_test_score': 64,
        'certificate': 0,
        'major_field': 6,
        'codingTest_score': 0
    },
    {
        'grade': 4,
        'depart': 1,
        'credit': 2,
        'in_school_award_cnt': 1,
        'out_school_award_cnt': 3,
        'national_competition_award_cnt': 3,
        'aptitude_test_score': 24,
        'certificate': 12,
        'major_field': 13,
        'codingTest_score': 2
    },
]

# 각 학생 데이터에 대한 예측 출력
for i, student_data in enumerate(student_data_list, start=1):
    predictions = predict_contest_winning_probabilities(student_data)
    print(f"학생 {i}의 대회별 예측:")
    for contest, prob in predictions.items():
        print(f"{contest}: {prob:.2f}%")
        print(contest[0])
    print()
