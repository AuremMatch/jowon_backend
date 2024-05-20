# models.py 또는 해당 코드를 실행할 파일에 추가
from contests.models import Contest

# 모든 Contest 객체 가져오기
contests = Contest.objects.all()

# 각 Contest 객체의 상금 필드를 숫자 형식으로 변환하고 쉼표 제거
for contest in contests:
    if contest.상금:
        # 쉼표 제거 후 숫자로 변환
        prize_str = contest.상금.replace(",", "")
        try:
            prize = int(prize_str)
            # 상금 필드를 숫자로 업데이트
            contest.상금 = prize
            contest.save()
        except ValueError:
            # 변환할 수 없는 값인 경우 예외 처리
            print(f"상금 데이터가 올바른 숫자 형식이 아닙니다: {contest.상금}")
