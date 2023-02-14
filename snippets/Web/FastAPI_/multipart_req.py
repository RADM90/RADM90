# Multi-part Requst Sample
import io
import json
import zipfile
import requests

dict_obj = {0: "Say Hello", 1: "Hello!", 2: "I am Ironman", 3: "No you are just JSON object"}
json_obj = json.dumps(dict_obj, sort_keys=True, indent=None)
headers = {"filename": f"test.mp4", "user_id": "{ID}"}

response = requests.get("http://localhost:8001/multipart", json=json_obj, headers=headers)
zip_binary = response.content
zip_file = io.BytesIO(zip_binary)

with zipfile.ZipFile(zip_file, "r") as myzip:
    myzip.extractall()

# 서버단
"""
from requests_toolbelt.multipart import decoder, encoder
from fastapi import FastAPI, UploadFile, File, Response, Request


@app.post("/multipart")
async def multipart(request: Request, files: List[UploadFile] = File(...)):
    # Multi-part Response 객체에는 JSON과 Binary Form의 Video를 묶어서 전송해야함
    # 마찬가지로 Request를 전송하는 송신단에서도 별도의 Decompression 작업이 필요하니 참고용으로만 볼 것
    file_name = request.headers.get('filename')
    user_id = request.headers.get('user_id')
    json_rcvd = request.json()
    for file in files:
        rcvd = await file.read()
        multipart_data = decoder.MultipartDecoder(await request.body(), content_type=request.headers["Content-Type"])
        parts = {part.headers[b"Content-Disposition"].decode().split(";")[1].split("=")[1][1:-1]: part.text for part in multipart_data.parts}  # Multi-part Request에서 데이터를 추출하는 방법 예시
        fields = {"data": (None, json.dumps(json_rcvd), "application/json")}
        fields["file"] = (file_name, rcvd, 'video/mp4')
        multipart_encoder = encoder.MultipartEncoder(fields=fields)
        response = Response(content=multipart_encoder.to_string(), media_type=multipart_encoder.content_type)
        response.headers["Content-Disposition"] = f'attachment; filename="data.zip"'
        return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)
"""

