"""
Valid from Python 3.5.0

모든 원소들의 최소공배수(LCM)는 각 원소를 최대공약수(GCD)로 나누어 곱한 값이므로
입력 배열 `arr`의 각 원소를 순회하며 최대공약수로 나눈 수를 곱하여 반환
"""
import math


def solution(arr):
    answer = arr[0]
    for num in arr:
        answer *= num // math.gcd(answer, num)
    return answer

