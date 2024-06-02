import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler

import seaborn as sns
import matplotlib.pyplot as plt
import shap

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False


# 대회별 최대, 최소값 설정
aptitude_test_max_min = {
    '중대한 사회 안전 이니까': (48, 12),
    '부산 도시브랜드 굿즈 디자인 공모전': (64, 16),
    '인천건축학생공모전': (68, 17),
    'GCGF 혁신 아이디어 공모': (40, 10),
    '웹 개발 콘테스트': (64, 16)
}

# 독립 변수 최대값, 최소값 설정
max_min = {
    'national_competition_award_cnt': (5, 0),
    'out_school_award_cnt': (5, 0),
    'in_school_award_cnt': (5, 0),
    'certificate': (12, 0),  # 5개의 자격증 합산
    'major_field': (13, 0),   # 5개의 주전공 합산
    'depart': (4, 0),
    'credit': (4.5, 1.0),
    'grade': (4, 1),
    'codingTest_score': (2, 0)
}

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

# 데이터 정규화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# TensorFlow SavedModel로부터 모델을 로드
loaded_model = tf.keras.models.load_model(r'C:\Mymodel\JongsulModel.h5')

# 모델 평가
mse, mae = loaded_model.evaluate(X_scaled, y)
print("평균 제곱 오차:", mse)
print("평균 절대 오차:", mae)

# 새로운 학생 데이터 예측
def predict_contest_winning_probabilities(new_student_data):
    new_student_df = pd.DataFrame([new_student_data], columns=X.columns)
    new_student_data_scaled = scaler.transform(new_student_df)
    predictions = loaded_model.predict(new_student_data_scaled)[0]
    
    # 확률값을 0과 100 사이의 값으로 변환
    predictions = np.clip(predictions, 0, 100)
    
    return {contest: prob for contest, prob in zip(aptitude_test_max_min.keys(), predictions)}


# 각 열의 평균보다 작거나 큰지 판단하는 함수 정의
def compare_with_average(student_data, average_values):
    comparisons = {}
    for column, value in student_data.items():
        if value < average_values[column]:
            comparisons[column] = "Unfit"
        elif value > average_values[column]:
            comparisons[column] = "Suitable"
        else:
            comparisons[column] = "Average"
    return comparisons

# 학생 데이터에 대해 열의 값이 평균보다 큰지 작은지 비교하여 반환
def visualize_comparison(student_data, average_values, column_order, color):
    comparisons = compare_with_average(student_data, average_values)
    columns = [col for col in column_order if col in student_data.keys()]
    values = [student_data[col] for col in columns]
    comparison_results = [comparisons[col] for col in columns]
    
    plt.figure(figsize=(10, 6))
    bars = plt.barh(columns, values, color=color, label='학생 데이터')
    
    for i in range(len(columns)):
        color = 'green' if comparison_results[i] == '큼' else 'red' if comparison_results[i] == '작음' else 'gray'
        plt.text(values[i] + 0.05, i, comparison_results[i], color=color, fontweight='bold', va='center')
    
    plt.xlabel('값')
    plt.ylabel('변수')
    plt.title('학생 데이터와 평균값 비교')
    plt.legend()
    plt.show()

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
    print()

# credit 열을 제외한 나머지 열 선택
independent_variables_only = df.drop(columns=['credit'] + list(aptitude_test_max_min.keys()))

# credit 열을 제외한 나머지 열의 평균 계산 및 정수로 반올림
average_values = independent_variables_only.mean().round().astype(int)

# credit 열의 평균 계산 및 정수로 반올림
credit_average = df['credit'].mean().round().astype(int)

# credit 열의 평균 값을 average_values에 추가하여 순서 조정
average_values = pd.concat([average_values, pd.Series({'credit': credit_average})])

# 결과 출력
print("credit 열을 제외한 나머지 열의 평균:")
print(average_values)
print()


# 각 학생 데이터에 대해 평균값과의 비교 출력
for i, student_data in enumerate(student_data_list, start=1):
    comparisons = compare_with_average(student_data, average_values)
    print(f"학생 {i}의 데이터와 각 열의 평균값 비교:")
    for column, comparison in comparisons.items():
        print(f"{column}: {comparison}")
    print()


# 각 학생 데이터에 대해 시각화하여 표시
colors = ['#FFAEC9', '#BEFFAA', '#FFFCAA', '#A4CEFF']
for i, student_data in enumerate(student_data_list, start=1):
    print(f"학생 {i}의 대회별 예측:")
    predictions = predict_contest_winning_probabilities(student_data)
    for contest, prob in predictions.items():
        print(f"{contest}: {prob:.2f}%")
    print()
    visualize_comparison(student_data, average_values, ['grade', 'depart', 'credit', 'in_school_award_cnt', 'out_school_award_cnt', 'national_competition_award_cnt', 
                                                        'aptitude_test_score', 'certificate', 'major_field', 'codingTest_score'], colors[i-1])

# 학생 데이터에 대한 거리 출력
for i, student_data in enumerate(student_data_list, start=1):
    print(f"학생 {i}의 변수 별 최대값으로부터의 거리:")
    for var_name, (max_val, min_val) in max_min.items():
        distance_from_max = max_val - student_data[var_name]
        distance_from_min = student_data[var_name] - min_val
        print(f"{var_name}: 최대값으로부터 {distance_from_max}, 최소값으로부터 {distance_from_min}")
    print()

# DeepExplainer를 사용하여 SHAP 값 계산
explainer = shap.DeepExplainer(loaded_model, X_scaled[:1000])
shap_values = explainer.shap_values(X_scaled[:1000])

# 클래스에 해당하는 실제 이름 정의
class_names = ['중대한 사회 안전 이니까', '부산 도시브랜드 굿즈 디자인 공모전', '인천건축학생공모전', 'GCGF 혁신 아이디어 공모', '웹 개발 콘테스트']

# SHAP 값 시각화
shap.summary_plot(shap_values, features=X_scaled[:1000], feature_names=X.columns, class_names=class_names, plot_type='bar', show=True)
