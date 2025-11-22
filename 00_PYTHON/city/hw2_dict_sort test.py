
country = {
        'Seoul'       : ['South Korea', 'Asia', '9,655,000'],
        'Tokyo'       : ['Japan', 'Asia', '14,110,000'],
        'Beijing'     : ['China', 'Asia', '21,540,000'],
        'London'      : ['United Kingdom', 'Europe', '14,800,000'],
        'Berlin'      : ['Germany', 'Europe', '3,426,000'],
        'Mexico City' : ['Mexico', 'America', '21,200,000']}
    
def dict_country(country) :
    for i, (key, value) in enumerate(country.items(), 1) : # 1부터 시작
        print(f'{[i]} {key}: {value} ')
        
# [1] Seoul: ['South Korea', 'Asia', '9,655,000']
# [2] Tokyo: ['Japan', 'Asia', '14,110,000']
# [3] Beijing: ['China', 'Asia', '21,540,000']
# [4] London: ['United Kingdom', 'Europe', '14,800,000']
# [5] Berlin: ['Germany', 'Europe', '3,426,000']
# [6] Mexico City: ['Mexico', 'America', '21,200,000']

# def dict_city(country, key=False, index=0, asc=True) : # [2]수도 오름차순, [3]인구수 내림차순() / dict.items() 및 sorted(reverse=True : 내림차순) : 기본값 오름차순 
#         if index == 0 : # [2]수도 오름차순
#             sorted_data = sorted(country.items(), key = lambda x : x[0])
#             for i, (city, value) in enumerate(sorted_data, 1) : 
#                 print(f'{[i]} {city:<12} : {value[0]:<15} {value[1]:<8} {value[2]:<5}')
#         elif index == 1 : # [3]인구수 내림차순()
#                 sorted_data = sorted(country.items(), key = lambda x : x[1][2], reverse=True)
#                 for i, (city, value) in enumerate(sorted_data, 1) : 
#                         print(f'{[i]} {city:<12} : {value[2]:<5}')

        
# dict_city(country, key=False, index=1, asc=True) 
# def print_city(country) :
#     key = input(f'출력할 도시 이름을 입력하세요: ')
#     if key in country :
#         print(f'도시 : {key}')
#         print(f'국가 : {country[key][0]}, 대륙 : {country[key][1]}, 인구수: {country[key][2]}')
#     else :
#         print(f' 도시이름: {key}은 key에 없습니다. ')

# print_city(country)     
 

def print_continent(country):
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
print_continent(country)              


# [1] Beijing : ['China', 'Asia', '21,540,000']
# [2] Berlin : ['Germany', 'Europe', '3,426,000']
# [3] London : ['United Kingdom', 'Europe', '14,800,000']
# [4] Mexico City : ['Mexico', 'America', '21,200,000']
# [5] Seoul : ['South Korea', 'Asia', '9,655,000']
# [6] Tokyo : ['Japan', 'Asia', '14,110,000']