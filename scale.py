import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd


# 엑셀 파일 경로
file_path = r'/Users/yundong-gyu/Documents/jowon_project/jongsulData.xlsx'
df = pd.read_excel(file_path)

# 데이터 전처리
def convert_to_numbers(lst):
    return [int(x) for x in lst.split(',')]

df['certificate'] = df['certificate'].apply(convert_to_numbers)
df['subject'] = df['subject'].apply(convert_to_numbers)
df['major_field'] = df['major_field'].apply(convert_to_numbers)
df = df.explode('certificate').explode('subject').explode('major_field')
df['certificate'] = df['certificate'].astype(int)
df['subject'] = df['subject'].astype(int)
df['major_field'] = df['major_field'].astype(int)

X = df.drop(['중대한 사회 안전 이니까', '부산 도시브랜드 굿즈 디자인 공모전', '인천건축학생공모전', 'GCGF 혁신 아이디어 공모', '웹 개발 콘테스트'], axis=1)
y = df[['중대한 사회 안전 이니까', '부산 도시브랜드 굿즈 디자인 공모전', '인천건축학생공모전', 'GCGF 혁신 아이디어 공모', '웹 개발 콘테스트']]

# 스케일러 학습 및 저장
scaler = StandardScaler()
scaler.fit(X)
np.save('predictor/scaler_mean.npy', scaler.mean_)
np.save('predictor/scaler_scale.npy', scaler.scale_)
