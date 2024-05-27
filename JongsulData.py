import pandas as pd
import numpy as np

# 데이터 생성
np.random.seed(0)  # 재현 가능성을 위해 난수 생성기 시드 설정

# 자격증 인덱스 랜덤 부여 함수
def generate_certificates(length) :
    return [','.join(map(str, np.random.randint(0, 50, size=5))) for i in range(length)]

# 부전공 인덱스 랜덤 부여 함수
def generate_subject(length) :
    subjects = []
    for _ in range(length) :
        d = np.random.randint(0,5)
        if d < 4 :
            # 수업은 난수 5개 받는데, 3개는 관련 종목으로 무조건 받는다.
            subjects.append(','.join(map(str, np.random.choice(range(d * 10, d * 10 + 10), size = 3, replace=False))) +
                           ',' + ','.join(map(str, np.random.choice(range(50), size=2, replace=True))))
        else :
            subjects.append(','.join(map(str, np.random.choice(range(20,30), size=3, replace=False))) +
                           ',' + ','.join(map(str, np.random.choice(range(50), size=2, replace=True))))
    return subjects

# 주전공 인덱스 랜덤 부여 함수
def generate_major_field(length) :
    major_field = []
    for _ in range(length) :
        d = np.random.randint(0,5)
        if d < 4 :
            # 주전공은 난수 2개 받는데, 학과 관련 주전공으로 받아올 확률이 높다.
            major_field.append(','.join(map(str, np.random.choice(range(d * 5, d * 5 + 5), size=2))))
        else :
            major_field.append(','.join(map(str, np.random.choice(range(20, 23), size=2))))
    return major_field


data = {
    # 독립변수
    # 학년
    'grade': np.random.randint(1, 5, size=10000),
    # 학과
    'depart': np.random.randint(0, 5, size=10000),
    # 학점
    'credit': np.round(np.random.uniform(1.0, 4.5, size=10000), 2),

    # 교내 수상 이력 갯수
    'in_school_award_cnt': np.random.randint(0, 5, size=10000),
    # 교외 수상 이력 갯수
    'out_school_award_cnt': np.random.randint(0, 5, size=10000),
    # 전국대회 수상 이력 갯수
    'national_competition_award_cnt': np.random.randint(0, 3, size=10000),

    # 자격증 인덱스
    'certificate': generate_certificates(10000),
    # 수업 인덱스
    'subject': generate_subject(10000),
    # 주전공 인덱스
    'major_field': generate_major_field(10000),
    # 코딩테스트 점수
    'codingTest_score': np.random.randint(0, 101, size=10000),

    #종속변수
    '중대한 사회 안전 이니까': np.random.randint(0, 11, size=10000) * 10,
    '부산 도시브랜드 굿즈 디자인 공모전': np.random.randint(0, 11, size=10000) * 10,
    '인천건축학생공모전': np.random.randint(0, 11, size=10000) * 10,
    'GCGF 혁신 아이디어 공모': np.random.randint(0, 11, size=10000) * 10,
    '웹 개발 콘테스트': np.random.randint(0, 11, size=10000) * 10
}


# 데이터프레임 생성
df = pd.DataFrame(data)

# grade, credit, in_school_award_cnt, codingTest_score 열을 모두 정수로 변환
df[['grade', 'credit', 'in_school_award_cnt', 'codingTest_score']] = df[['grade', 'credit', 'in_school_award_cnt', 'codingTest_score']].astype(int)

# 데이터프레임 출력
print(df)

num_one_grade = (df['grade'] == 1).sum()
print("grade가 1인 행의 개수:", num_one_grade)
num_two_grade = (df['grade'] == 2).sum()
print("grade가 2인 행의 개수:", num_two_grade)
num_three_grade = (df['grade'] == 3).sum()
print("grade가 3인 행의 개수:", num_three_grade)
num_four_grade = (df['grade'] == 4).sum()
print("grade가 4인 행의 개수:", num_four_grade)

print(df['grade'].unique())

#엑셀 파일로 저장
df.to_excel('jongsulData.xlsx', index=False)