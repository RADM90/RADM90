import requests
import json

dict_obj = {0: "Say Hello", 1: "Hello!", 2: "I am Ironman", 3: "No you are just JSON object"}
json_obj = json.dumps(dict_obj, sort_keys=True, indent=None)  # 사실 이 과정은 requests 라이브러리는에서 알아서 처리하므로 굳이 필요없음.
# json 파라미터에 dict 데이터 넣어도 무방하나, JSON 특성 상 key값에 String이 아닌 데이터가 들어가는건 권장되지 않음
# (불가능한 것은 아니나 표준을 벗어남)

headers = {"filename": f"test.mp4", "user_id": "{ID}"}
response = requests.post("http://localhost:8001/", json=dict_obj, headers=headers)
print(response.headers)