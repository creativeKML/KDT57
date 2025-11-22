# 1. 지하철 각 노선별 최대 하차 인원을 막대그래프로 표시하고, 하차인원을 출력하시오.
# n 제출 파일:	hw03_subway.py
# n 출근 시간대: 07:00~08:59
# n 사용 파일: subwaytime.csv	또는 subway.xls
# - 07:00~07:59 하차: index[11],	08:00~08:59 하차: index	[13]

# # 실행결과
# 출근 시간대 1호선 최대 하차역:	종각역,	하차인원:	364,228명
# 출근 시간대 2호선 최대 하차역:	역삼역,	하차인원:	485,263명
# 출근 시간대 3호선 최대 하차역:	양재(서초구청)역,	하차인원:	320,395명
# 출근 시간대 4호선 최대 하차역:	충무로역,	하차인원:	231,715명
# 출근 시간대 5호선 최대 하차역:	여의도역,	하차인원:	346,856명
# 출근 시간대 6호선 최대 하차역:	공덕역,	하차인원:	130,219명
# 출근 시간대 7호선 최대 하차역:	가산디지털단지역,	하차인원:	491,650명

# 1. 지하철 각 노선별 최대 하차 인원 막대그래프로 표시, 하차인원을 출력하시오.

import pandas as pd
import csv
import matplotlib.pyplot as plt
import koreanize_matplotlib
from tabulate import tabulate

# 노선 리스트, 역정보 리스트, 노선별 최대 하차역
subway_lines = ['1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선']
max_by_line = {} # [0]key= '1호선', '2호선' / [1]value = (역이름, 하차인원)

# 하차 인원이 많은 역 이름 찾기
with open('subwaytime.csv', encoding='utf-8-sig') as f :
    data = csv.reader(f)
    next(data)
    next(data)

    # 노선리스트 데이터만 확인
    for row in data :
        if row[1] in subway_lines :
            row[4:] = map(int, row[4:])

            passenger_num = row[11] + row[13]
            line_name = row[1]
            station_name = row[3]

        if line_name not in max_by_line :
            max_by_line[line_name] = (station_name, passenger_num)
        else :
            if passenger_num > max_by_line[line_name][1] :
                max_by_line[line_name] = (station_name, passenger_num)

for line in  subway_lines :
    if line in max_by_line :
        station, passenger = max_by_line[line]
        print(f'출근 시간대 {line} 최대 하차역: {station}역, 하차인원: {passenger:,}명')

# 막대그래프 생성
x_labels = [f'{line}{max_by_line[line][0]}' for line in subway_lines if line in max_by_line]
y_values = [max_by_line[line][1] for line in subway_lines if line in max_by_line]

plt.figure(figsize=(12,8))
plt.title('출근 시간대 지하철 노선별 최대 하차 인원 및 하차역', size = 16)

plt.bar(range(len(y_values)), y_values, color='steelblue')
plt.xticks(range(len(x_labels)), x_labels, rotation = 70, fontsize=8) 
plt.tight_layout()
plt.show()
