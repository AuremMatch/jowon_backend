from rest_framework.decorators import api_view
from rest_framework.response import Response
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from users.models import Score


@api_view(['POST'])
def predict_view(request):
    # Score 모델에서 데이터를 가져옵니다. id와 user 필드는 제외합니다.
    scores = Score.objects.values_list('grade', 'depart', 'credit', 'in_school_award_cnt', 'out_school_award_cnt',
                                   'national_competition_award_cnt', 'certificate', 'subject', 'major_field',
                                   'codingTest_score')

    # Score 모델에서 가져온 데이터를 Pandas DataFrame으로 변환합니다.
    score_data = pd.DataFrame(scores)
    
    # NaN 값을 0으로 대체합니다. (필요에 따라 다르게 처리할 수 있습니다)
    score_data = score_data.fillna(0)
    
    # 스케일러 로드 및 데이터 변환
    scaler = StandardScaler()
    score_scaled = scaler.fit_transform(score_data)  # 스케일러를 적용하기 전에 fit_transform 사용
    
    # 모델 로드 및 예측
    model = tf.keras.models.load_model('model.h5')
    predictions = model.predict(score_scaled)
    
    # 예측 결과를 JSON 형태로 반환합니다.
    return Response({'predictions': predictions.tolist()})



# @api_view(['GET', 'POST'])
# def predict_view(request):
#     if request.method == 'GET':
#         # GET 요청의 경우 이 부분에서 예측 결과를 반환하도록 처리합니다.
#         # 이 예제에서는 단순히 샘플 데이터를 예측하여 반환합니다.
#         sample_data = {
#             'grade': 3,
#             'depart': 3,
#             'credit': 3,
#             'in_school_award_cnt': 2,
#             'out_school_award_cnt': 0,
#             'national_competition_award_cnt': 1,
#             'certificate': '13,28,5,9,37',
#             'subject': '10,20,15,16,17',
#             'major_field': '14,7',
#             'codingTest_score': 80
#         }

#         new_student_data = pd.DataFrame(sample_data, index=[0])

#         def convert_to_numbers(lst):
#             return [int(x) for x in lst.split(',')]

#         new_student_data['certificate'] = new_student_data['certificate'].apply(convert_to_numbers)
#         new_student_data['subject'] = new_student_data['subject'].apply(convert_to_numbers)
#         new_student_data['major_field'] = new_student_data['major_field'].apply(convert_to_numbers)
#         new_student_data = new_student_data.explode('certificate').explode('subject').explode('major_field')
#         new_student_data['certificate'] = new_student_data['certificate'].astype(int)
#         new_student_data['subject'] = new_student_data['subject'].astype(int)
#         new_student_data['major_field'] = new_student_data['major_field'].astype(int)

#         # 스케일러 로드 및 데이터 변환
#         scaler = StandardScaler()
#         scaler.mean_ = np.load('predictor/scaler_mean.npy')
#         scaler.scale_ = np.load('predictor/scaler_scale.npy')
#         new_student_scaled = scaler.transform(new_student_data)

#         # 모델 로드 및 예측
#         model = tf.keras.models.load_model('model.h5')
#         predictions = model.predict(new_student_scaled)

#         # 예측 결과를 JSON 형태로 반환
#         return Response({'predictions': predictions.tolist()})
    
#     elif request.method == 'POST':
#         # POST 요청에 대한 처리
#         data = request.data
#         new_student_data = pd.DataFrame({
#             'grade': [data['grade']],
#             'depart': [data['depart']],
#             'credit': [data['credit']],
#             'in_school_award_cnt': [data['in_school_award_cnt']],
#             'out_school_award_cnt': [data['out_school_award_cnt']],
#             'national_competition_award_cnt': [data['national_competition_award_cnt']],
#             'certificate': [data['certificate']],
#             'subject': [data['subject']],
#             'major_field': [data['major_field']],
#             'codingTest_score': [data['codingTest_score']]
#         })
#         def convert_to_numbers(lst):
#             return [int(x) for x in lst.split(',')]
#         new_student_data['certificate'] = new_student_data['certificate'].apply(convert_to_numbers)
#         new_student_data['subject'] = new_student_data['subject'].apply(convert_to_numbers)
#         new_student_data['major_field'] = new_student_data['major_field'].apply(convert_to_numbers)
#         new_student_data = new_student_data.explode('certificate').explode('subject').explode('major_field')
#         new_student_data['certificate'] = new_student_data['certificate'].astype(int)
#         new_student_data['subject'] = new_student_data['subject'].astype(int)
#         new_student_data['major_field'] = new_student_data['major_field'].astype(int)
#         scaler = StandardScaler()
#         scaler.mean_ = np.load('predictor/scaler_mean.npy')
#         scaler.scale_ = np.load('predictor/scaler_scale.npy')
#         new_student_scaled = scaler.transform(new_student_data)
#         model = tf.keras.models.load_model('model.h5')
#         predictions = model.predict(new_student_scaled)
#         return Response({'predictions': predictions.tolist()})