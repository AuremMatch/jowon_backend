import pandas as pd
import numpy as np
import random

# 데이터 생성
np.random.seed(0)  # 재현 가능성을 위해 난수 생성기 시드 설정

# 자격증 인덱스 랜덤 부여 함수 수정
def generate_certificates(length):
    return [sum(random.sample(range(6), 3)) for _ in range(length)]

"""
# 대회별 중요한 자격증 설정값
important_certificates = {
    '부산 도시브랜드 굿즈 디자인 공모전': ['제품디자인기술사(5)', '시각디자인기사(4)', '제품디자인기사(3)', '웹 디자인 기능사(2)', '컴퓨터그래픽스운용기능사(1)'],
    '인천건축학생공모전': ['건축설비기사(5)', '건축기사(4)', '도시계획기사(3)', '실내건축기사(2)', '조경기사(1)'],
    '중대한 사회 안전 이니까': ['멀티미디어콘텐츠제작전문가(5)', '문예창작사(4)', '논술지도사(3)', '독서지도사(2)', '한국어 교육능력검정시험(1)'],
    'GCGF 혁신 아이디어 공모': ['경영지도사(5)', '사회조사분석사(4)', '금융재난관리사(3)', '자산관리사(2)', '재무위험관리사(1)'],
    '웹 개발 콘테스트': ['정보처리기사(5)', '정보통신기사(4)', '데이터분석(3)', '리눅스마스터(2)', '정보기술자격(1)']

    여기서 각 대회에서 중요한 자격증일수록 점수가 높다. 
    즉 사용자가 대회에서 해당 자격증이 있는지 체크할건데, 많이 체크할 수록 점수가 높아질거다.
    ３개를 체크 가능한데 높은 순위의 자격증만 체크할 경우 12이고, min값은 0일것이다. 
    이때 중요도가 높은 자격증은 점수가 높으므로 체크한 항목에 그것이 존재하면 점수가 높을 것이다. 
}
"""

# 주전공 인덱스 랜덤 부여 함수
def generate_major_field(length):
    return [sum(random.sample(range(8), 2)) for _ in range(length)]

"""
depart는 1에서 3사이의 난수를 받는다, 가중치를 곱해주므로 높을 수록 확률이 증가한다.
높은 점수일 수록 해당 대회에서 중요한 학과이다.
"""

"""
# 대회별 중요한 각 주 전공 리스트
important_major_field = {
    '부산 도시브랜드 굿즈 디자인 공모전': ['제품 디자인'（７）, '그래픽 디자인'（６）, '인터랙션 디자인'（５）, '서비스 디자인'（４）, '가구 디자인'（３）, '포장 디자인'（２）, '환경 디자인'（１）],
    '인천건축학생공모전': ['도시 계획', '구조 공학', '건축 디자인', '건축 기술', '실내 건축', '환경 디자인', '건축 역사 및 이론']
    '중대한 사회 안전 이니까': ['저널리즘', '광고학', '방송학', '홍보학', '커뮤니케이션 이론', '디지털 미디어', '미디어 이론 및 연구']
    'GCGF 혁신 아이디어 공모': ['경영전략', '마케팅', '경영 과학', '회계학', '인적자원관리', '운영관리', '재무관리']
    '웹 개발 콘테스트': ['소프트웨어 공학', '웹 및 애플리케이션 개발', '데이터베이스', '네트워크 보안', '컴퓨터 시스템 및 네트워크', '인공지능', '컴퓨터 공학']

    여기서 각 대회에서 중요한 자격증일수록 점수가 높다. 
    즉 사용자가 대회에서 해당 자격증이 있는지 체크할건데, 많이 체크할 수록 점수가 높아질거다.
    2개를 체크 가능한데 높은 순위의 자격증만 체크할 경우 13이고, min값은 0일것이다. 
    이때 중요도가 높은 자격증은 점수가 높으므로 체크한 항목에 그것이 존재하면 점수가 높을 것이다. 
}
"""

data = {
    'grade': np.random.randint(1, 5, size=50000),  # 50,000개로 변경
    'depart': np.random.randint(1, 4, size=50000),  # 50,000개로 변경 (1, 2, 3의 값만 갖도록 변경)
    'credit': np.round(np.random.uniform(1.0, 4.5, size=50000), 2),  # 50,000개로 변경
    'in_school_award_cnt': np.random.randint(0, 5, size=50000),  # 50,000개로 변경
    'out_school_award_cnt': np.random.randint(0, 5, size=50000),  # 50,000개로 변경
    'national_competition_award_cnt': np.random.randint(0, 3, size=50000),  # 50,000개로 변경
    'aptitude_test_score': np.random.randint(10, 64, size=50000),  # 50,000개로 변경
    'certificate': generate_certificates(50000),  # 초기화,  # 50,000개로 변경
    'major_field': generate_major_field(50000),  # 50,000개로 변경
    'codingTest_score': np.random.randint(0, 3, size=50000)  # 50,000개로 변경
}

# 데이터프레임 생성
df = pd.DataFrame(data)

# 기본 대회 가중치 정의
basic_weights = {
    'national_competition_award_cnt': 0.25,
    'out_school_award_cnt': 0.20,
    'in_school_award_cnt': 0.15,
    'aptitude_test_score': 0.10,
    'certificate': 0.08,
    'major_field': 0.07,
    'depart': 0.06,
    'credit': 0.04,
    'grade': 0.03,
    'codingTest_score': 0.02
}

# '웹 개발 콘테스트' 대회 가중치 정의
software_weights = {
    'national_competition_award_cnt': 0.25,
    'out_school_award_cnt': 0.20,
    'in_school_award_cnt': 0.15,
    'aptitude_test_score': 0.10,
    'codingTest_score': 0.08,
    'major_field': 0.07,
    'certificate': 0.06,
    'depart': 0.04,
    'credit': 0.03,
    'grade': 0.02
}

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
    if contest == '웹 개발 콘테스트':
        weights = software_weights
    else:
        weights = basic_weights
    df[contest] = df.apply(lambda row: calculate_probability(row, weights, max_min, aptitude_test_max_min, contest), axis=1)

# 데이터프레임 출력
print(df.head())

# 엑셀 파일로 저장
df.to_excel('jongsulData.xlsx', index=False)