import json

dic = {'4': 5, '6': 7}

"""Encoding"""
json_str = json.dumps(dic, ensure_ascii=False, separators=(',', ':'), sort_keys=True, indent=None)
# dumps: dict()를 JSON 문자열로 변환 '{"4": 5, "6": 7}'

with open("test.json", "w+", encoding='utf-8') as f:
    json.dump(dic, f)
# dump: JSON 형식의 IO로 변환된 dict()를 파일로 저장


"""Decoding"""
with open("test.json", "r+", encoding='utf-8') as f:
    data = json.load(f)
# load: JSON 형식의 파일을 읽어와서 json 객체로 변환

print(json.loads(json_str))
# loads: JSON 문자열을 읽어와서 json 객체로 변환
