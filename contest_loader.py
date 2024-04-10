import json

# JSON 파일 읽기
with open("loads.json", 'r') as f:
    contest = json.load(f)

# 새로운 데이터 리스트 생성
new_list = []

# 각 항목에 대해 반복
for a in contest:
    # "wpoint" 필드가 있는지 확인하고 있다면 삭제
    if "wpoint" in a["fields"]:
        del a["fields"]["wpoint"]
    
    # "" 키가 있는지 확인하고 있다면 삭제
    if "" in a["fields"]:
        del a["fields"][""]
    
    # 수정된 데이터를 새로운 리스트에 추가
    new_data = {"model": "contests.contest"}
    new_data["fields"] = a["fields"]
    new_list.append(new_data)

# 수정된 데이터를 load.json 파일에 쓰기
with open("loadss.json", 'w', encoding='UTF-8') as f:
    json.dump(new_list, f, ensure_ascii=False, indent=2)