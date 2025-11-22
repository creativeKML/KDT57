'''
	과제 1-2. 최근 30년간 열대야 발생 횟수를 라인 그래프로 출력 
	- 1980년 ~ 2024년까지 대구 기온 데이터에서 연도별 열대야의 총 횟수 계산 
	- 열대야(tropical night): 여름밤 최저 기온이 25도 이상인 현상 
	
'''
import csv 
import matplotlib.pyplot as plt 
import koreanize_matplotlib


def draw_line_graph(year_count_list, start_year, end_year):   # ⭐[참조에 의한 호출 : call-by-reference] 리스트 -> 함수로 전달 -> 내부에서 값 채워옴
	xtick_list = []

	for year in range(start_year, end_year+1):
		xtick_list.append(year)
	
	plt.figure(figsize=(18, 4))
	plt.bar(xtick_list, year_count_list)
	plt.title(f'{start_year}년도에서 {end_year}년도까지 열대야 현황')	
	plt.xlabel('year')
	plt.xticks(xtick_list, fontsize=8)
	plt.ylabel('열대야 수')
	plt.show()

def print_list_data(list, year):
	'''
	list[]의 값을 한 줄에 10개씩 화면에 출력 (90년대, 2000년대 )
	'''
	for i in range(len(list)):
		print(f'{i+year}년: {list[i]:2d}회', end= ' ')
		if (i+1) % 10 == 0:
			print()
		i += 1
	print()

def get_tropical_night_count(data, start_year, end_year, year_count_list):
	'''
	start_year에서 end_year까지 각 연도별 6월~9월 사이에 발생한 열대야의 총 횟수를 계산	 
	'''
	next(data)
	lowest_temp = 0.0

	for row in data:
		if row[3] != '':
			date_string = row[0].split('-')
			year = int(date_string[0])
			month = int(date_string[1])
			if year >= start_year and year <= end_year:
				if month >= 6 and month <= 9:
					lowest_temp = float(row[3])
					if lowest_temp >= 25.0:
						year_count_list[year-start_year] += 1               # ⭐[패턴] 각각 연도 누적 카운트


def main():
	start_year = 1990
	end_year = 2024
	year_count_list = [0] * (end_year - start_year + 1)


	f = open('daegu-utf8.csv', encoding='utf-8-sig')
	data = csv.reader(f)

	# start_year부터 각 연도별 열대야 횟수를 계산하여 list에 저장 
	get_tropical_night_count(data, start_year, end_year, year_count_list) 

	# 연도별 열대야 현황을 화면 출력
	print_list_data(year_count_list, start_year) 

	# 각 연도별 열대야 횟수를 그래프로 출력 
	draw_line_graph(year_count_list, start_year, end_year)

	# 10년 주기별 누적횟수 그래프로 작성 
	f.close()


main()
