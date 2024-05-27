
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import os


# 엑셀 파일 경로
file_path = r'/Users/yundong-gyu/Documents/jowon_project/jongsulData.xlsx'
df = pd.read_excel(file_path)

# 데이터 전처리 및 모델 학습
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

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
np.save('predictor/scaler_mean.npy', scaler.mean_)
np.save('predictor/scaler_scale.npy', scaler.scale_)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(5)
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)
loss, mae = model.evaluate(X_test, y_test)
print("Test Loss:", loss)

model.save('model.h5')