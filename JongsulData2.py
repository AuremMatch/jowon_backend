import pandas as pd
import numpy as np
import random

# 데이터 생성
np.random.seed(0)  # 재현 가능성을 위해 난수 생성기 시드 설정

# 자격증 인덱스 랜덤 부여 함수 수정
def generate_certificates(length):
    return [sum(random.sample(range(6), 3)) for _ in range(length)]

# 주전공 인덱스 랜덤 부여 함수
def generate_major_field(length):
    return [sum(random.sample(range(8), 2)) for _ in range(length)]

data = {
    'grade': np.round(np.random.uniform(1.0, 4.5, size=50000), 2),
    'github_commit_count': np.random.randint(1, 50, size=50000),
    'baekjoon_score': np.random.randint(1, 12, size=50000),
    'programmers_score': np.random.randint(1, 12, size=50000),
    'certificate_count': np.random.randint(0, 10, size=50000),
    'senior': np.random.randint(1, 4, size=50000),
    'depart': np.random.randint(1, 3, size=50000),
    'courses_taken': np.random.randint(1, 3, size=50000),
    'major_field': generate_major_field(50000),
    'bootcamp_experience': np.random.randint(1, 2, size=50000),
    'in_school_award_cnt': np.random.randint(0, 10, size=50000),
    'out_school_award_cnt': np.random.randint(0, 10, size=50000),
    'coding_test_score': np.random.randint(1, 5, size=50000),
    'certificate_score': generate_certificates(50000),
    'aptitude_test_score': np.random.randint(10, 64, size=50000),
}

# 데이터프레임 생성
df = pd.DataFrame(data)

# 기본 대회 가중치 정의
basic_weights = {
    'grade': 0.10,
    'senior': 0.20,
    'certificate_score': 0.20,
    'certificate_count': 0.20,
    'major_field': 0.10,
    'depart': 0.05,
    'courses_taken': 0.05,
    'bootcamp_experience': 0.05,
    'in_school_award_cnt': 0.10,
    'out_school_award_cnt': 0.10,
    'coding_test_score': 0.05,
    'aptitude_test_score': 0.10,
}

# '웹 개발 콘테스트' 대회 가중치 정의
software_weights = {
    'grade': 0.05,
    'senior': 0.20,
    'github_commit_count': 0.20,
    'baekjoon_score': 0.20,
    'programmers_score': 0.20,
    'major_field': 0.05,
    'depart': 0.05,
    'courses_taken': 0.05,
    'bootcamp_experience': 0.10,
    'in_school_award_cnt': 0.05,
    'out_school_award_cnt': 0.05,
    'coding_test_score': 0.10,
    'aptitude_test_score': 0.10,
}

# '웹 개발 콘테스트' 대회 가중치 정의
contest_weights = {
    'grade': 0.05,
    'senior': 0.05,
    'github_commit_count': 0.05,
    'baekjoon_score': 0.05,
    'programmers_score': 0.05,
    'major_field': 0.05,
    'depart': 0.05,
    'courses_taken': 0.05,
    'bootcamp_experience': 0.05,
    'in_school_award_cnt': 0.05,
    'out_school_award_cnt': 0.05,
    'coding_test_score': 0.05,
    'aptitude_test_score': 0.30,
}

# 대회별 최대, 최소값 설정
aptitude_test_max_min = {
    '언어 예측값': (48, 12),
    '디자인 예측값': (64, 16),
    '건축 예측값': (68, 17),
    '현재 대회 예측값': (40, 10),
    'it 예측값': (64, 16)
}

# 독립 변수 최대값, 최소값 설정
max_min = {
    'grade': (4.5, 1.0),
    'github_commit_count': (50, 1),
    'baekjoon_score': (12, 1),
    'programmers_score': (12, 1),
    'certificate_count': (10, 0),
    'senior': (4, 1),
    'depart': (3, 1),
    'courses_taken': (3, 1),
    'major_field': (13, 0),
    'bootcamp_experience': (2, 1),
    'in_school_award_cnt': (10, 0),
    'out_school_award_cnt': (10, 0),
    'coding_test_score': (5, 0),
    'certificate_score': (12, 0),
}

# 확률 계산 함수
def calculate_probability(row, weights, max_min, apt_max_min, contest):
    score = 0
    for col, weight in weights.items():
        if col == 'aptitude_test_score':
            max_val, min_val = apt_max_min[contest]
        else:
            max_val, min_val = max_min[col]

        scaled_value = (row[col] - min_val) / (max_val - min_val)
        score += scaled_value * weight

    probability = min(100, max(0, score * 100))  # 점수를 0에서 100 사이의 확률로 변환
    probability = round(probability, 2)  # 소수점 아래 둘째 자리에서 반올림
    return probability

# 종속 변수(대회에서 우승할 확률) 계산
for contest in aptitude_test_max_min.keys():
    if contest == 'it 예측값':
        weights = software_weights
    elif contest == "현재 대회 예측값":
        weights = contest_weights
    else:
        weights = basic_weights
    df[contest] = df.apply(lambda row: calculate_probability(row, weights, max_min, aptitude_test_max_min, contest), axis=1)

# 데이터프레임 출력
print(df.head())

# 엑셀 파일로 저장
df.to_excel('jongsulData5.xlsx', index=False)
