import os

# 운영체제 기본 경로 구분자
print(os.path.sep)  # 변경하려면 별도 값을 해당 변수에 선언


def path_creator(str_path):
    # 경로가 존재하지 않을 때 경로를 생성하는 기능
    if os.path.exists(str_path) is False:
        print("Creating Directory:", str_path)
        os.makedirs(str_path)

