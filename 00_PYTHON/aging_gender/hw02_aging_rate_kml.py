# 2. 대한민국 전체 행정구역중에서 고령화지수가 가장 높은 지역의 이름과 고령인구,	
# 유소년인구 수, 고령화지수를 화면에 출력하고 유소년인구수와 고령인구수 비율을
# 파이차트로 작성하시오. (hw02_aging_rate.py)
# - age.csv 파일 사용

# - 최대값?
#  실행결과(화면 출력 내용)
# OOOOOOO 고령인구:	OOOO 명,	유소년인구:	OOO 명,	노령화지수:	12033.3%

# 고령화지수가 가장 높은 지역 이름과 고령인구, 유소년인구 수, 고령화지수 출력
# - 고령 인구수:	65세 이상
# - 유소년 인구수:	0-14세
# - 유소년 인구수가 0인 행정구역은 제외(divide	zero 예외 발생)
# - 고령화지수 = 고령인구 / 유소년인구 * 100
import csv
import matplotlib.pyplot as plt
import koreanize_matplotlib

def draw_pie_chart(city, population_list, label_list):
    plt.pie(population_list, labels=label_list, autopct='%.1f%%',
            startangle=90, colors=['skyblue', 'steelblue'], textprops={'fontsize': 8})
    plt.legend(loc=1)
    plt.title(city + " 고령화 지수")
    plt.show()

def get_population(row, start_age, end_age):
    '''
    age.csv 파일에서 나이를 이용한 인구수 구하기
    - 나이를 해당 인덱스로 변환: 인덱스= 나이 + 3	
    '''
    population = 0
    start_index = start_age + 3
    end_index = end_age + 3
    for num in row[start_index: end_index+1]:
        num = num.replace(',', '')
        num = int(num)
        population += num
    return population

def get_aging_population(city):
    youth_range = (0, 14)  # 0세 ~ 14세까지
    old_range = (65, 100)  # 65세 ~ 100세 이상
    old_population = 0
    youth_population = 0
    label_list = ['유소년 인구', '고령인구']
    
    f = open('age.csv', encoding='euc-kr')
    data = csv.reader(f)
    next(data)  # 헤더 정보 건너뜀
    
    for row in data:
        # 괄호와 코드 제거하여 깔끔한 지역명으로 비교
        clean_city_name = row[0].split('(')[0].strip()
        if city in clean_city_name:
            youth_population = get_population(row, youth_range[0], youth_range[1])
            old_population = get_population(row, old_range[0], old_range[1])
            break
    f.close()
    
    if youth_population == 0:  # 유소년 인구가 0인 경우 제외
        return None
        
    aging_rate = round((old_population*100)/youth_population, 1)
    print(f'{clean_city_name} 고령인구: {old_population:,}명, '
          f'유소년인구: {youth_population:,}명, '
          f'노령화지수: {aging_rate}%')
    draw_pie_chart(clean_city_name, [youth_population, old_population], label_list)
    
    return aging_rate

def find_highest_aging_city():
    '''고령화지수가 가장 높은 지역을 찾는 함수'''
    max_aging_rate = 0
    max_city = ""
    max_youth = 0
    max_old = 0
    
    f = open('age.csv', encoding='euc-kr')
    data = csv.reader(f)
    next(data)  # 헤더 정보 건너뜀
    
    for row in data:
        # 괄호와 코드 제거하여 깔끔한 지역명 추출
        city_name = row[0].split('(')[0].strip()
        youth_population = get_population(row, 0, 14)  # 0-14세
        old_population = get_population(row, 65, 100)  # 65-100세
        
        # 유소년 인구가 0인 지역은 제외 (divide zero 예외 방지)
        if youth_population == 0:
            continue
            
        aging_rate = (old_population * 100) / youth_population
        
        if aging_rate > max_aging_rate:
            max_aging_rate = aging_rate
            max_city = city_name
            max_youth = youth_population
            max_old = old_population
    
    f.close()
    
    # 결과 출력
    print(f'{max_city} 고령인구: {max_old:,}명, '
          f'유소년인구: {max_youth:,}명, '
          f'노령화지수: {round(max_aging_rate, 1)}%')
    
    # 파이차트 그리기
    label_list = ['유소년 인구', '고령인구']
    draw_pie_chart(max_city, [max_youth, max_old], label_list)

# 실행부분
print("=== 고령화지수가 가장 높은 지역 찾기 ===")
find_highest_aging_city()

print("\n=== 특정 도시 검색 ===")
city = input("노령화 지수를 분석할 도시 이름: ")
get_aging_population(city)