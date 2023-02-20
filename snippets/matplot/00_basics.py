import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12, 7))  # 가장 바탕이 되는 틀 (Figure), 사이즈: 인치

ax1 = fig.add_subplot(1, 2, 1)  # 서브플롯 ax
ax2 = fig.add_subplot(1, 2, 2)  # 서브플롯을 여러 개 쓰려면 위치 지정

x1 = [1, 2, 3]
x2 = [3, 2, 1]

plt.plot(x1)  # 서브플롯 ax1에 x1 데이터 그리기 // ax1.plot(x1)과 동일
plt.plot(x2)  # 서브플롯 ax2에 x2 데이터 그리기 // ax2.plot(x2)과 동일

# plt로 그리면 plt.gcf().get_axes()로 다시 서브플롯 객체를 받아서 사용 가능

"""하나의 플롯에 여러 그래프 그리기"""
ax1.plot([1, 1, 1], color='r', label='1')  # 빨강(한 글자 지정)
ax1.plot([1, 2, 3], color='forestgreen')  # 초록(색상명 지정)
ax1.plot([3, 3, 3], color='#000000')  # 검정(HEX코드)
ax1.plot([1, 2, 3], [1, 2, 3])  # 선 그래프
ax1.bar([1, 2, 3], [1, 2, 3])  # 막대 그래프

ax1.legend()  # 범례 추가
ax1.set_title('Basic Plot')  # 도표 제목 설정 (set_@@@() 메서드)
ax1.get_title()  # 도표 제목 불러오기 (get_@@@() 메서드)

ax1.set_xticks([0, 1, 2])  # (x)축에 적히는 수의 위치 지정
ax1.set_xticklabels(['zero', 'one', 'two'])  # (x)축에 적히는 수의 라벨 지정

ax1.text(x=1, y=2, s='This is Text')
ax1.annotate(text='This is Annotate', xy=(1, 2),
             xytext=(1.2, 2.2),
             arrowprops=dict(facecolor='black'),
             )
