'''
	과제 1-1. 열대야 횟수 계산 
	- 특정 연도의 대구 기온 데이터에서 열대야의 총 횟수 계산 

	- 열대야(tropical night): 여름밤 최저 기온이 25도 이상인 현상 
	
'''
import csv 

def get_tropical_night(data, check_year): # data : csv 리더객체, check_year : 조사할 연도
	'''
	특정 연도(check_year)의 6월부터 9월사이의 총 열대야 횟수 계산 
	- 최저 기온: 25도 이상 
	'''
	# csv의 첫 번째 줄(헤더)을 건너뜁니다. (next()로 한 줄 스킵)
	next(data)
	tropical_night_count=0  # 열대야가 발생한 횟수 세기 위한 변수 : 초기값 0
	lowest_temp = 0.0       # 최저기온을 저장할 임시 변수

	for row in data:        # csv 데이터 각 줄을 반복
		if row[3] != '':    # row[3] : '최저기온 컬럼 // 비어있지 않은 경우에만 처리
			date_string = row[0].split('-')
			year = int(date_string[0])
			month = int(date_string[1])
			day = int(date_string[2])
			'''
			2024년 6월부터 9월 사이의 열대야 조사 
			'''
			if year == check_year:
				if month >= 6 and month <=9:
					lowest_temp = float(row[3])
					if lowest_temp >= 25.0:
						print(f'{month}-{day:2d}: {lowest_temp}')
						tropical_night_count += 1

	print(f'{check_year}년 대구의 총 열대야 횟수: {tropical_night_count}')



def main():
	#check_year = 2024 
	check_year = int(input('열대야를 계산할 연도를 입력하세요: '))
	
	f = open('daegu-utf8.csv', encoding='utf-8-sig')
	data = csv.reader(f)
	get_tropical_night(data, check_year) 
	f.close()


main()