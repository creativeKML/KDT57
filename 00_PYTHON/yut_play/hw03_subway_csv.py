'''
과제 3. 출근 시간대 지하철 하차 인원 분석
- 각 지하철 호선별(1~7호선) 최대 하차 역 및 하차인원 수 출력 
'''
import csv 
import matplotlib.pyplot as plt
import koreanize_matplotlib 

def draw_bar_chart(result_dict):
	xticks_list = []
	population_list = []

	for key in result_dict: # key: 1호선, 2호선, ... 
		station_name, population = result_dict.get(key)		
		population_list.append(population)
		# key : 1호선, 2호선, 3호선 ... 7호선
		xticks_list.append(key + ' ' + station_name) # ['1호선 종각', '2호선 역삼', ...] 

	plt.figure(dpi=100)
	plt.bar(range(7), population_list)
	plt.xticks(range(7), xticks_list, rotation=80)
	plt.title('출근 시간대 지하철 노선별 최대 하차 인원 및 하차역', size=16)
	plt.tight_layout()
	plt.show()


def print_dict(result_dict):	
	for key in result_dict:                  #'1호선' [지하철역, 하차인원수]
		station, population = result_dict.get(key)
		print(f'출근 시간대 {key} 최대 하차역: {station}역, 하차인원: {population:,}명')
	
		
def main():
	#max_population = 0	# 최대값 비교 기준값 
	subway_lines=['1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선']
	result_dict = dict()	# {'1호선': [지하철역, 하차인원], '2호선': [지하철역, 하차인원], ...}
	max_population = [0] * 7
	f = open('subwaytime.csv', encoding='utf-8-sig')
	data = csv.reader(f)

	index = 0
	for row in data:
		for i in range(len(subway_lines)):			
			if row[1] == subway_lines[i]:
				population = int(row[11]) + int(row[13])
				if population > max_population[i]:
					max_population[i] = population
					max_station = row[3] 
					result_dict[subway_lines[i]] = [max_station, population] # 키가 같으니까, 계속 값이 업데이트됨
				
	f.close()
	print_dict(result_dict)
	draw_bar_chart(result_dict)


main()