import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# bar(): 기본적인 막대그래프
# barh(): bar()의 피벗인 수평 막대그래프

fig, axes = plt.subplots(1, 2, figsize=(12, 7))
x = list('ABCDE')
y = np.array([1, 2, 3, 4, 5])

clist = ['blue', 'gray', 'gray', 'gray', 'red']
color = 'green'

axes[0].bar(x, y, color=clist)  # 색상 문자열 리스트 적용
axes[1].barh(x, y, color=color)  # 단일 색상 문자열 적용

# ===

student = pd.read_csv('./StudentsPerformance.csv')  # 데이터 불러오기
student.sample(5)
student.info()
student.describe(include='all')

# 성별에 따른 인종, 민족 분포 확인
group = student.groupby('gender')['race/ethnicity'].value_counts().sort_index()
display(group)
print(student['gender'].value_counts())

# Multiple Bar Plot
fig, axes = plt.subplots(1, 2, figsize=(15, 7), sharey=True)  # sharey 속성을 이용하여 y축의 범위 공유 가능
axes[0].bar(group['male'].index, group['male'], color='royalblue')
axes[1].bar(group['female'].index, group['female'], color='tomato')

"""
# y축의 범위를 개별적으로 조정하려면 아래와 같이 적용
# 단, 각 그룹간 비교가 어렵다는 단점이 있음

fig, axes = plt.subplots(1, 2, figsize=(15, 7))
axes[0].bar(group['male'].index, group['male'], color='royalblue')
axes[1].bar(group['female'].index, group['female'], color='tomato')

for ax in axes:
    ax.set_ylim(0, 200)
"""

# Stacked Bar Plot
group_cnt = student['race/ethnicity'].value_counts().sort_index()
axes[0].bar(group_cnt.index, group_cnt, color='darkgray')
axes[1].bar(group['male'].index, group['male'], color='royalblue')
axes[1].bar(group['female'].index, group['female'], bottom=group['male'], color='tomato')  # bottom 파라미터로 하단 공간 확보 가능
