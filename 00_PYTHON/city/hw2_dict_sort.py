# Python 과제 #02

# def dict_sort() 함수 기능
# 1. 전체 데이터 출력
# 2. 수도 이름(key 기준) 오름차순 출력
# 3. 모든 도시의 인구수 내림차순 출력
# 4. 특정 도시의 정보 출력
# 5. 대륙별 인구수 계산 및 출력
# 6. 프로그램 종료

#                  [key]
# city = country['Seoul'] 
# #             value[key][0] value[key][1] value[key][2]
# print(city) # ['South Korea', 'Asia', '9,655,000']

# city = country['Seoul'][0]
# print(city) # South Korea

# enumerate(country.items(), 1) :
# [1] Seoul: ['South Korea', 'Asia', 9655000]
# [2] Tokyo: ['Japan', 'Asia', 14110000]

def menu():
    print('-' * 41)
    print(f'1. 전체 데이터 출력')
    print(f'2. 수도 이름 오름차순 출력')
    print(f'3. 모든 도시의 인구수 내림차순 출력')
    print(f'4. 특정 도시의 정보 출력')
    print(f'5. 대륙별 인구수 계산 및 출력')
    print(f'6. 프로그램 종료')
    print('-' * 41)

def main():
# 0. 딕셔너리 생성 및 정렬 프로그램
##  key : 수도 이름, value : 국가명, 대륙, 인구수
#   key                                           value
#   [0]            |                               [1]
#   key             [0]국가명:country_name    [1]대륙:continent   [2]인구수:population
    country = {
        'Seoul'       : ['South Korea', 'Asia', '9,655,000'],
        'Tokyo'       : ['Japan', 'Asia', '14,110,000'],
        'Beijing'     : ['China', 'Asia', '21,540,000'],
        'London'      : ['United Kingdom', 'Europe', '14,800,000'],
        'Berlin'      : ['Germany', 'Europe', '3,426,000'],
        'Mexico City' : ['Mexico', 'America', '21,200,000']}   

    while True :
        menu()
        try:
            menu_choice = int(input(f'메뉴를 입력하세요: '))

            if menu_choice == 1 :
                dict_country(country)

            elif menu_choice == 2 :
                dict_city(country, index=0, desc=False) # 수도 오름차순
    
            elif menu_choice == 3 :
                dict_city(country, index=1, desc=True) # 인구수 내림차순

            elif menu_choice == 4 :
                print_city(country)
    
            elif menu_choice == 5 :
                print_continent(country)

            elif menu_choice == 6 :
                print(f' 프로그램을 종료합니다.')
                break
                
            else: 
                print('1~6 사이의 숫자를 입력하세요.')

        except ValueError :
            print('숫자를 입력하세요.')

def dict_country(country) : # [메뉴 1] 전체 데이터 출력
    for i, (key, value) in enumerate(country.items(), 1) : # 1부터 시작
        print(f'{[i]} {key}: {value} ')
        
def dict_city(country, index=0, desc=True) :
    if index == 0 : # [메뉴 2]수도 오름차순
        sorted_data = sorted(country.items(), key = lambda x : x[0], reverse=desc)
        for i, (city, value) in enumerate(sorted_data, 1) : 
            print(f'{[i]} {city:<12} : {value[0]:<15} {value[1]:<8} {value[2]:<5}')

    elif index == 1 : # [메뉴 3]인구수 내림차순()
        sorted_data = sorted(country.items(), key = lambda x : int(x[1][2].replace(',','')), reverse=desc)
        for i, (city, value) in enumerate(sorted_data, 1) : 
            print(f'{[i]} {city:<12} : {int(value[2].replace(",","")):,}')              

def print_city(country) : # [메뉴 4] 특정 도시 정보
    key = input(f'출력할 도시 이름을 입력하세요: ')
    if key in country :
        print(f'도시 : {key}')
        print(f'국가 : {country[key][0]}, 대륙 : {country[key][1]}, 인구수: {country[key][2]}')
    else :
        print(f' 도시이름: {key}은 key에 없습니다. ')

def print_continent(country): # [메뉴 5] 대륙별 인구수 
    name = input('대륙 이름을 입력하세요 (Asia, Europe, America): ')
    found = False
    sum = 0

    for city, info in country.items():
        if info[1] == name:
            print(f"{city:<12} : {info[2]}")
            sum = sum + int(info[2].replace(",", ""))
            found = True

    if not found:
        print(f"'{name}'에 해당하는 데이터가 없습니다.")
    else: 
        print(f'{name} 전체 인구수 : {sum:,}')

if __name__ == '__main__':
    main()


