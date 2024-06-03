from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import io
import base64
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model

# 최대값과 최소값 설정
aptitude_test_max_min = {
    '중대한 사회 안전 이니까': (48, 12),
    '부산 도시브랜드 굿즈 디자인 공모전': (64, 16),
    '인천건축학생공모전': (68, 17),
    'GCGF 혁신 아이디어 공모': (40, 10),
    '웹 개발 콘테스트': (64, 16)
}

max_min = {
    'national_competition_award_cnt': (5, 0),
    'out_school_award_cnt': (5, 0),
    'in_school_award_cnt': (5, 0),
    'certificate': (12, 0),
    'major_field': (13, 0),
    'depart': (4, 0),
    'credit': (4.5, 1.0),
    'grade': (4, 1),
    'codingTest_score': (2, 0)
}

# 평균값 설정
average_values = {
    'grade': 2.5,
    'depart': 2,
    'credit': 3,
    'in_school_award_cnt': 2,
    'out_school_award_cnt': 1.5,
    'national_competition_award_cnt': 1,
    'aptitude_test_score': 45,
    'certificate': 8,
    'major_field': 9,
    'codingTest_score': 1.5
}

# 모델과 스케일러를 전역 변수로 설정하여 재사용
model = None
scaler = None

def load_model_and_scaler():
    global model, scaler

    # 데이터 로드 및 전처리
    df = pd.read_excel('jongsulData.xlsx')
    X = df.drop(columns=aptitude_test_max_min.keys())
    y = df[list(aptitude_test_max_min.keys())]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = load_model(r'C:\Mymodel\JongsulModel.h5')
    mse, mae = model.evaluate(X_scaled, y)
    print("평균 제곱 오차:", mse)
    print("평균 절대 오차:", mae)

load_model_and_scaler()

@csrf_exempt
def predict_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # 요청 데이터 처리
        students = data.get('students')
        if not students:
            return JsonResponse({'error': 'No student data provided'}, status=400)

        predictions = []
        graphs = []

        for i, student in enumerate(students):
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

                # 그래프 생성
                buf = visualize_comparison(new_student_data, average_values, ['grade', 'depart', 'credit', 'in_school_award_cnt', 'out_school_award_cnt', 'national_competition_award_cnt', 'aptitude_test_score', 'certificate', 'major_field', 'codingTest_score'])
                # Base64로 인코딩하여 리스트에 추가
                graphs.append(base64.b64encode(buf.getvalue()).decode('utf-8'))
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'predictions': predictions, 'graphs': graphs})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def predict_contest_winning_probabilities(new_student_data):
    new_student_df = pd.DataFrame([new_student_data])
    new_student_data_scaled = scaler.transform(new_student_df)
    predictions = model.predict(new_student_data_scaled)[0]
    predictions = np.clip(predictions, 0, 100)
    return {contest: float(prob) for contest, prob in zip(aptitude_test_max_min.keys(), predictions)}

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

def visualize_comparison(student_data, average_values, column_order):
    comparisons = compare_with_average(student_data, average_values)
    columns = [col for col in column_order if col in student_data.keys()]
    values = [student_data[col] for col in columns]
    comparison_results = [comparisons[col] for col in columns]

    plt.figure(figsize=(10, 6))
    bars = plt.barh(columns, values, label='학생 데이터')

    for bar, result in zip(bars, comparison_results):
        bar_color = 'green' if result == "Suitable" else 'red' if result == "Unfit" else 'blue'
        bar.set_color(bar_color)
    
    plt.xlabel('Values')
    plt.title('Student Data Comparison with Average')
    plt.legend()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    return buf
