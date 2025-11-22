# 1. 대구광역시 전체 및 9개 
# 구,군별 (중구, 동구, 서구, 남구, 북구, 수성구, 달서구, 달성군, 군위군)
#  남녀 비율을 각각의 파이 차트로 구현하세요. (hw02_gender_rate.py)
# gender.csv 파일 사용
# 2x5 형태의 subplot으로 총 10개 파이 차트 출력
# (중구, 동구, 서구, 남구, 북구, 수성구, 달서구, 달성군, 군위군 포함)

import csv
import pandas as pd
import matplotlib.pyplot as plt
import re
import koreanize_matplotlib  # 한글폰트 지원

# 파일 읽기
f = open('gender.csv', encoding='euc-kr')
# csv.reader : 1회용 읽기 => f.seek(0): 리셋 필요 => list 변환
data = list(csv.reader(f)) 
f.close()

header = data[0]
data = data[1:]
# 데이터 확인하기
# data_list = list(data)
# print(data_list[0])
# f.close()

# 대구광역시 관련 지역 목록
city_list = []

for row in data :
    if '대구광역시' in row[0] :
        str_list = re.split('[()]', row[0]) # 괄호 제거
        city = str_list[0].strip()
        city_list.append(city)
print(f'대구광역시 지역목록 : {city_list}')
# 대구광역시 지역목록 : ['대구광역시  ', '대구광역시 중구 ', 
# '대구광역시 동구 ', '대구광역시 서구 ', '대구광역시 남구 ', 
# '대구광역시 북구 ', '대구광역시 수성구 ', '대구광역시 달서구 ', 
# '대구광역시 달성군 ', '대구광역시 군위군 ']

# 남녀 인구수 리스트
male_count = []
female_count = []

for city in city_list :
    for row in data :
        if city == row[0].split('(')[0].strip():
                male = int(row[104].replace(',', ''))
                female = int(row[207].replace(',', ''))
                male_count.append(male)
                female_count.append(female)
                break


# 각 지역별 인구수 출력
for i in range(len(city_list)):
    print(f'{city_list[i]} : (남:{male_count[i]:,} 여:{female_count[i]:,})')

# 서브플롯 파이차트
fig, axes = plt.subplots(2, 5, figsize=(20, 10))
fig.suptitle('대구광역시 구/군별 남녀 인구 비율', fontsize=16, fontweight='bold')  # subtitle → suptitle

colors = ['cornflowerblue', 'darkorange']
labels = ['남성', '여성']

# 각 지역별 파이차트 생성
for i in range(len(city_list)) :
    row = i // 5  # 행 인덱스 (0 또는 1)
    col = i % 5   # 열 인덱스 (0~4)

    # 해당 지역의 남녀 인구수
    population = [male_count[i], female_count[i]]
    total = sum(population)

    # 비율 계산
    male_ratio = (male_count[i] / total) * 100
    female_ratio = (female_count[i] / total) * 100

    # 파이차트 그리기
    axes[row, col].pie(population,
                       colors=colors,
                       autopct='%1.1f%%',  # 비율 표시 추가
                       startangle=90,
                       textprops={'fontsize':10})
    
    # 차트별 제목
    axes[row, col].set_title(city_list[i], fontsize=12, pad=20)

# 차트 레이아웃
plt.tight_layout()
plt.subplots_adjust(top=0.93)  # 제목 공간 확보
plt.show()
