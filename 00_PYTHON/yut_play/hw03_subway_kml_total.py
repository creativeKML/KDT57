import csv
import matplotlib.pyplot as plt
import koreanize_matplotlib

subway_lines = ['1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선']
max_by_lines = {}

x_labels = []
y_values = []

with open('subwaytime.csv', encoding='utf-8-sig') as f :
    data = csv.reader(f)
    next(data)
    next(data)

    for row in data : 
        if row[1] in subway_lines :
            row[4:] = map(int, row[4:])
            passenger_num = row[11] + row[13]
            station_name = row[3]
            line = row[1]

            if line in max_by_lines : 
                current_max = list(max_by_lines[line].values())[0]
                if passenger_num > current_max :
                    max_by_lines[line] = {station_name : passenger_num}

            else :
                max_by_lines[row[1]] = {station_name : passenger_num}

for line in max_by_lines : 
    for station_name, passenger_num in max_by_lines[line].items() :
        print(f'출근 시간대 {line} 최대 하차역 : {station_name}, 하차 인원{passenger_num}명')
        x_labels.append(line + station_name)
        y_values.append(passenger_num)

plt.figure(figsize=(12,8))
plt.title('출근 시간대 지하철 노선별 최대 하차 인원 및 하차역', size = 16)
plt.bar(range(len(y_values)), y_values, color='steelblue')
plt.xticks(range(len(x_labels)), x_labels, rotation=70, fontsize=8) 
plt.tight_layout()
plt.show()   

# --------------------------------------------------------------------------------------------
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
with open('subwaytime.csv') as f :
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

# --------------------------------------------------------------------------------------------
# 지하철 출근시간대 최대 하차역 분석 - 단계별 학습 가이드
## 전체 목표
# 출근 시간대에 각 지하철 노선별로 가장 많은 사람이 하차하는 역을 찾고, 이를 막대그래프로 시각화하기

# 1. **CSV 파일 처리**: csv.reader를 사용한 파일 읽기
# 2. **데이터 타입 변환**: map() 함수를 사용한 문자열→정수 변환
# 3. **딕셔너리 활용**: 중첩 딕셔너리를 사용한 데이터 저장
# 4. **조건문과 반복문**: if문과 for문을 활용한 데이터 필터링
# 5. **matplotlib**: 한글 폰트 설정과 막대그래프 생성
# 6. **데이터 시각화**: 축 라벨, 제목, 색상 등 그래프 꾸미기

# 딕셔너리가 어떻게 채워지는지 단계별로 보기

# 1단계: 빈 딕셔너리로 시작
max_by_lines = {}
print(f"1단계 - 초기 상태: {max_by_lines}")

# 2단계: 첫 번째 데이터가 들어올 때
# 가상의 첫 번째 row 데이터라고 가정
row_1 = ['기타', '1호선', '기타', '서울역', 0, 0, 0, 0, 0, 0, 0, 5000, 0, 8000, 0]
#                              역명             07-08시    08-09시
line_1 = row_1[1]          # '1호선'
station_1 = row_1[3]       # '서울역'  
passenger_1 = row_1[11] + row_1[13]  # 5000 + 8000 = 13000

print(f"\n=== 첫 번째 데이터 처리 ===")
print(f"노선: {line_1}")
print(f"역명: {station_1}")
print(f"승객수: {passenger_1}")

# 1호선이 딕셔너리에 없으므로 새로 추가
if line_1 not in max_by_lines:
    max_by_lines[line_1] = (station_1, passenger_1)
    print(f"2단계 - 첫 데이터 추가 후: {max_by_lines}")

# 3단계: 같은 노선의 다른 역 데이터가 들어올 때
row_2 = ['기타', '1호선', '기타', '종각역', 0, 0, 0, 0, 0, 0, 0, 3000, 0, 5000, 0]
line_2 = row_2[1]          # '1호선' (같은 노선)
station_2 = row_2[3]       # '종각역'
passenger_2 = row_2[11] + row_2[13]  # 3000 + 5000 = 8000

print(f"\n=== 두 번째 데이터 처리 (같은 노선) ===")
print(f"노선: {line_2}")
print(f"역명: {station_2}")
print(f"승객수: {passenger_2}")

# 1호선이 이미 있으므로 값 비교
if line_2 in max_by_lines:
    current_max = max_by_lines[line_2][1]  # 튜플의 두 번째 요소 (승객수)
    print(f"기존 최대값: {current_max}")
    print(f"새로운 값: {passenger_2}")
    
    if passenger_2 > current_max:
        max_by_lines[line_2] = (station_2, passenger_2)
        print(f"더 큰 값이므로 업데이트!")
    else:
        print(f"기존 값이 더 크므로 유지")
    
    print(f"3단계 - 비교 후: {max_by_lines}")

# 4단계: 다른 노선 데이터가 들어올 때
row_3 = ['기타', '2호선', '기타', '강남역', 0, 0, 0, 0, 0, 0, 0, 15000, 0, 20000, 0]
line_3 = row_3[1]          # '2호선' (새로운 노선)
station_3 = row_3[3]       # '강남역'
passenger_3 = row_3[11] + row_3[13]  # 15000 + 20000 = 35000

print(f"\n=== 세 번째 데이터 처리 (새로운 노선) ===")
print(f"노선: {line_3}")
print(f"역명: {station_3}")
print(f"승객수: {passenger_3}")

if line_3 not in max_by_lines:
    max_by_lines[line_3] = (station_3, passenger_3)
    print(f"새로운 노선이므로 추가")

print(f"4단계 - 최종 결과: {max_by_lines}")

print(f"\n=== 딕셔너리 구조 분석 ===")
for line, data in max_by_lines.items():
    station_name = data[0]  # 튜플의 첫 번째 요소
    passenger_count = data[1]  # 튜플의 두 번째 요소
    print(f"노선: {line}")
    print(f"  └ 최대 하차역: {station_name}")
    print(f"  └ 하차 인원: {passenger_count:,}명")

print(f"\n=== 실제 구현 코드 ===")

# 실제 for문에서는 이렇게 동작합니다:
for row in data:
    if row[1] in subway_lines:
        line = row[1]
        station = row[3]
        passengers = row[11] + row[13]
        
        if line in max_by_lines:
            if passengers > max_by_lines[line][1]:  # 튜플의 두 번째 요소와 비교
                max_by_lines[line] = (station, passengers)
        else:
            max_by_lines[line] = (station, passengers)

# --------------------------------------------------------------------------------------------
'''
max_by_line = {
    '1호선': {'서울역': 15000},
    '2호선': {'강남역': 20000}
}

# 현재 처리 중인 데이터
row[1] = '1호선'  # 노선명
passenger_num = 18000  # 현재 역의 하차인원

# 단계별 실행
step1 = max_by_line[row[1]]           # {'서울역': 15000}
step2 = step1.values()                # dict_values([15000])
step3 = list(step2)                   # [15000]
step4 = step3[0]                      # 15000

# 최종 비교
if 18000 > 15000:  # True
    # 새로운 최대값으로 업데이트
'''
## 4단계: 결과 출력

### 질문 4-1: 각 노선별 최대 하차역 정보를 출력하세요
# - 딕셔너리를 반복하면서 출력
# - "출근 시간대 {노선} 최대 하차역: {역명}, 하차인원: {인원:,}명" 형태로 출력
for line in max_by_line :
    for station_name, passenger_num in max_by_line[line].items() :
        print(f'출근 시간대 {line} 최대 하차역 : {station_name}, 하차인원: {passenger_num}명')

### 질문 4-2: 그래프용 데이터를 준비하세요
# - x축 라벨: 노선명 + 역명 조합
# - y축 값: 하차인원 수
        x_labels.append(line + station_name)
        y_values.append(passenger_num)

## 5단계: 막대그래프 생성

### 질문 5-1: 그래프 기본 설정을 하세요
# - figure 크기를 (12, 8)로 설정
# - 제목을 "출근 시간대 지하철 노선별 최대 하차 인원 및 하차역"으로 설정
plt.figure(figsize=(12, 8))
plt.title('출근 시간대 지하철 노선별 최대 하차 인원 및 하차역')

### 질문 5-2: 막대그래프를 생성하세요
# - plt.bar() 함수 사용
# - x축: range(len(y_values))
# - y축: y_values
# - 색상: 'steelblue'
plt.bar(range(len(y_values)), y_values, color = 'steelblue')

### 질문 5-3: x축 라벨을 설정하세요
# - plt.xticks() 함수 사용
# - rotation=70, fontsize=8로 설정하여 읽기 쉽게 조정
plt.xticks(range(len(x_labels)), x_labels, rotation=70, fontsize=8)

### 질문 5-4: y축 라벨을 설정하세요
# - plt.ylabel() 함수를 사용하여 "하차인원(명)" 설정
plt.ylabel('하차인원(명)')

### 질문 5-5: 그래프를 출력하세요
# - plt.tight_layout()으로 레이아웃 조정
# - plt.show()로 그래프 출력
plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------------------------
# 기본적인 튜플 언패킹
data = ('서울역', 120000)
station, passenger = data
print(station)  # 서울역
print(passenger) # 120000

# 리스트 언패킹
data = ['강남', 250000]
station, passenger = data
print(station) # 강남
print(passenger) # 250000

# 여러 개 동시에 언패킹
a, b, c = 1, 2, 3
print(a, b, c) # 1 2 3

# 언패킹 + 반복문
data = [('1호선', '종각'), ('2호선', '강남'), ('3호선', '고속터미널')]
for line, station in data :
    print(f'(line) -> {station}')
# (line) -> 종각
# (line) -> 강남
# (line) -> 고속터미널

# 필요없는 값 _로 처리
data = ('3호선', '고속터미널', 123456)
line, station, _ = data # passenger 삭제
print(line)    # 3호선
print(station) # 고속터미널

# *을 사용한 가변 언패킹
a, *b = [1,2,3,4,5] # 첫 1개, 나머지
print(a) # 1
print(b) # [2,3,4,5]
*a, b = [1,2,3,4,5] # 나머지, 마지막 1개
print(a) # [1,2,3,4]
print(b) # 5

# def f(*args) : 여러개 인자 튜플로 받음
def f(a, b, c):
    print(a, b, c)
values = [1, 2, 3]
# 리스트(또는 튜플)의 값을 하나씩 풀어서 전달
f(*values) # 1 2 3

# 함수를 정의할 때 *args를 쓰면,
# 들어오는 모든 인자를 하나의 튜플로 받음
def f(*args):
    print("받은 인자:", args)
    for arg in args:
        print("값:", arg)
f(10, 20, 30)
# 받은 인자: (10, 20, 30)
# 값: 10
# 값: 20
# 값: 30

# **kwargs(키워드 인자 언패킹)
# kwargs = keyword argumens
# 함수에 키=값 형식 인자 전달받을 때 사용

# 딕셔너리 언패킹은 다름
my_dict = {'a':10, 'b':20}
for key in my_dict :
    print(key) # a, b

for key, value in my_dict.items():
    print(key, value) # a 10, b 20
