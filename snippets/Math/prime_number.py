"""
1) 입력받은 값이 2보다 작을 경우(1일 경우) False 반환
2) 2부터 n의 제곱근까지 모든 수를 확인하며 n이 해당 수로 나눠질 경우 False 반환
"""


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True
