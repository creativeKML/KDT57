import sys
from matplotlib import font_manager, pyplot as plt, rc
import numpy as np
import pandas as pd
from tabulate import tabulate
import os
import seaborn as sns


# # 1. 엑셀파일 병합 및 저장(car_data.xlsx)
# file_directory = '../PROJECT_OPENDATA_4/'
# files = [
#     '2020년_06월_자동차_등록자료_통계.xlsx',
#     '2021년_06월_자동차_등록자료_통계.xlsx',
#     '2022년_06월_자동차_등록자료_통계.xlsx',
#     '2023년_06월_자동차_등록자료_통계.xlsx',
#     '2024년_06월_자동차_등록자료_통계.xlsx',
#     '2025년_06월_자동차_등록자료_통계.xlsx'
# ]

# all_data = []

# # 최종 데이터프레임의 컬럼 정의
# final_columns = ['gender', 'age', 'total', 'Seoul', 'Busan', 'Daegu', 'Incheon',
#                  'Gwangju', 'Daejeon', 'Ulsan', 'Sejong', 'Gyeonggi', 'Gangwon', 'Chungbuk', 'Chungnam',
#                  'Jeonbuk', 'Jeonnam', 'Gyeongbuk', 'Gyeongnam', 'Jeju']

# for file_name_only in files:
#     try:
#         # 경로와 파일명을 os.path.join을 사용하여 결합 (운영체제 호환성을 위함)
#         file_path = os.path.join(file_directory, file_name_only)
#         year = int(file_name_only[:4])
        
#         # 엑셀 파일 읽기. '04.성별_연령별' 시트의 세 번째 행을 헤더로 사용
#         df = pd.read_excel(file_path, sheet_name='04.성별_연령별', header=2)
        
#         # 컬럼 개수가 예상과 다를 경우 예외 처리
#         if len(df.columns) != len(final_columns):
#             raise ValueError(f"'{file_name_only}' 파일의 컬럼 개수가 예상과 다릅니다. (예상: {len(final_columns)}, 실제: {len(df.columns)})")
        
#         # 미리 정의된 컬럼명으로 변경
#         df.columns = final_columns

#         # 'gender' 컬럼의 NaN 값을 바로 위 행의 값으로 채움
#         df['gender'] = df['gender'].ffill()
        
#         # 'age'와 'gender' 컬럼에서 필요 없는 행을 제거
#         df = df[~df['age'].isin(['법인 및 사업자', '합계'])]
#         df = df[~df['gender'].isin(['기타', '합계'])]
        
#         # 'Year' 컬럼 추가
#         df['Year'] = year
        
#         all_data.append(df)
#         print(f'✓ {year}년 데이터 읽음: {len(df)}행')
#     except FileNotFoundError:
#         print(f"✗ 오류: {file_path} 파일을 찾을 수 없습니다.")
#     except ValueError as ve:
#         print(f"✗ 오류: {file_path} 문제가 발생했습니다 - {ve}")
#     except Exception as e:
#         print(f"✗ 오류: {file_path} 오류가 발생했습니다 - {e}")

# if all_data:
#     # 모든 데이터를 하나로 병합
#     result = pd.concat(all_data, ignore_index=True)

#     # 'Year' 컬럼을 맨 앞으로 이동
#     cols = ['Year'] + [col for col in result.columns if col != 'Year']
#     result = result[cols]
    
#     # 엑셀 파일로 저장
#     result.to_excel('car_gender_data.xlsx', index=False)
#     print(f'\n✓ 총 {len(result)}행이 car_data.xlsx에 저장되었습니다.')
#     print(tabulate(result.head(), headers='keys', tablefmt='psql'))
# else: 
#     print('종료합니다.')
# -----------------------------------------------------------------------------------------
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터 불러오기
car_data = pd.read_excel('../PROJECT_OPENDATA_4/car_gender_data.xlsx')

# 지역명 매핑 (영문 -> 한글)
city_map = {
    'Seoul': '서울',
    'Busan': '부산', 
    'Daegu': '대구',
    'Incheon': '인천',
    'Gwangju': '광주',
    'Ulsan': '울산'
}

cities = ['Seoul', 'Busan', 'Daegu', 'Incheon', 'Gwangju', 'Ulsan']
years = car_data['Year'].unique()
age_order = ['10대 이하', '20대', '30대', '40대', '50대', '60대', '70대', '80대', '90대이상']


# -----------------------------------------------------------------------------------------
# [1] 주요 도시별 연도별 남녀 차량 등록 현황 (꺾은선 그래프)
print("[1] 주요 도시별 연도별 남녀 차량 등록 현황")

plt.figure(figsize=(20, 10))

# 공통 y축 범위 및 눈금 설정
y_min = 100000
y_max = 2100000
y_ticks = list(range(y_min, y_max + 1, 200000))  # 200,000 단위 눈금

for i, city in enumerate(cities):
    city_name = city_map[city]

    # 도시별 남성/여성 데이터
    male_data = car_data[(car_data['gender'] == '남성') & (car_data['age'] != '계')].groupby('Year')[city].sum()
    female_data = car_data[(car_data['gender'] == '여성') & (car_data['age'] != '계')].groupby('Year')[city].sum()

    plt.subplot(2, 3, i + 1)

    # 꺾은선 그래프 (남성/여성)
    plt.plot(years, male_data, marker='o', label='남성', color='skyblue')
    plt.plot(years, female_data, marker='s', label='여성', color='lightcoral')

    plt.title(f'{city_name} 연도별 남녀 차량 등록', fontweight='bold')
    plt.xlabel('연도')
    plt.ylabel('등록 대수 (만 대)')
    plt.xticks(years)
    
    # 공통 y축 범위 및 눈금 설정
    plt.ylim(y_min, y_max)
    plt.yticks(y_ticks, [f'{int(tick / 10000)}' for tick in y_ticks])  # 만 단위 표시

    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=8)

plt.tight_layout()
plt.savefig('car_gender_plot_1_final.png', dpi=150)
plt.show()
plt.close()
# -----------------------------------------------------------------------------------------
# [2] 2025년 지역별 연령대별 남녀 차량 등록 현황 (막대 그래프)
print("\n[2] 2025년 지역별 연령대별 남녀 차량 등록 현황")

df_2025 = car_data[(car_data['Year'] == 2025) & (car_data['age'] != '계')]

plt.figure(figsize=(20, 10))

# Define the common y-axis range and ticks for the bar plots
y_min = 0
y_max = 800000
y_ticks = [0, 100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000]

for i, city in enumerate(cities):
    city_name = city_map[city]
    
    male_data = df_2025[df_2025['gender'] == '남성'].set_index('age')[city].reindex(age_order, fill_value=0)
    female_data = df_2025[df_2025['gender'] == '여성'].set_index('age')[city].reindex(age_order, fill_value=0)
    
    x = np.arange(len(age_order))
    width = 0.35

    plt.subplot(2, 3, i + 1)
    plt.bar(x - width/2, male_data.values, width, label='남성', color='skyblue')
    plt.bar(x + width/2, female_data.values, width, label='여성', color='lightcoral')
    
    plt.title(f'{city_name} 연령대별 등록현황', fontweight='bold')
    plt.ylabel('등록 대수 (만 대)')
    
    # Set the common y-axis range and adjust y-ticks for readability
    plt.ylim(y_min, y_max)
    plt.yticks(y_ticks, [f'{int(tick / 10000)}' for tick in y_ticks])
    
    plt.xticks(x, age_order, rotation=45, ha='right', fontsize=9)
    plt.grid(axis='y', alpha=0.3)
    plt.legend()

plt.tight_layout()
plt.savefig('car_gender_plot_2.png', dpi=150)
plt.show()
plt.close()

# -----------------------------------------------------------------------------------------
print("\n[3] 연도별 주요 연령대별 남녀 자동차 등록 현황")

ages_to_plot = ['20대', '30대', '40대', '50대', '60대', '70대']
df_filtered = car_data[car_data['age'] != '계']

plt.figure(figsize=(20, 10))

# Define the common y-axis range and ticks for the bar plots
y_min = 0
y_max = 3000000
y_ticks = [0, 500000, 1000000, 1500000, 2000000, 2500000, 3000000]

for i, age_group in enumerate(ages_to_plot):
    df_age = df_filtered[df_filtered['age'] == age_group]
    
    male_data = df_age[df_age['gender'] == '남성'].set_index('Year')['total']
    female_data = df_age[df_age['gender'] == '여성'].set_index('Year')['total']
    
    x = np.arange(len(years))
    width = 0.35

    plt.subplot(2, 3, i + 1)
    plt.bar(x - width/2, male_data.values, width, label='남성', color='skyblue')
    plt.bar(x + width/2, female_data.values, width, label='여성', color='lightcoral')
    
    plt.title(f'{age_group} 연령대', fontweight='bold')
    plt.xticks(x, years)
    plt.xlabel('연도')
    plt.ylabel('등록 대수 (만 대)')
    
    # Set the common y-axis range and adjust y-ticks for readability
    plt.ylim(y_min, y_max)
    plt.yticks(y_ticks, [f'{int(tick / 10000)}' for tick in y_ticks])
    
    plt.legend()
    plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('car_gender_plot_3.png', dpi=150)
plt.show()
plt.close()

# -----------------------------------------------------------------------------------------
# [4] 2020년 vs 2025년 인구 피라미드
print("\n[4] 2020년 vs 2025년 주요 지역별 성별-연령별 자동차 등록 현황")

df_compare = car_data[(car_data['Year'].isin([2020, 2025])) & (car_data['age'] != '계')]

plt.figure(figsize=(20, 10))
y_pos = np.arange(len(age_order))

for i, city in enumerate(cities):
    city_name = city_map[city]
    
    df_2025 = df_compare[df_compare['Year'] == 2025]
    df_2020 = df_compare[df_compare['Year'] == 2020]
    
    male_2025 = df_2025[df_2025['gender'] == '남성'].set_index('age')[city].reindex(age_order, fill_value=0)
    female_2025 = df_2025[df_2025['gender'] == '여성'].set_index('age')[city].reindex(age_order, fill_value=0)
    
    male_2020 = df_2020[df_2020['gender'] == '남성'].set_index('age')[city].reindex(age_order, fill_value=0)
    female_2020 = df_2020[df_2020['gender'] == '여성'].set_index('age')[city].reindex(age_order, fill_value=0)
    
    plt.subplot(2, 3, i + 1)
    plt.barh(y_pos, -male_2025, label='2025 남성', color='skyblue', alpha=0.8)
    plt.barh(y_pos, -male_2020, label='2020 남성', color='steelblue', alpha=0.5)
    plt.barh(y_pos, female_2025, label='2025 여성', color='lightcoral', alpha=0.8)
    plt.barh(y_pos, female_2020, label='2020 여성', color='indianred', alpha=0.5)
    
    ticks = plt.xticks()[0]
    plt.xticks(ticks, [f'{abs(int(x))//10000}만' if abs(x) > 0 else '0' for x in ticks])
    
    plt.yticks(y_pos, age_order)
    plt.title(city_name, fontweight='bold')
    plt.xlabel('등록 대수')
    plt.grid(axis='x', alpha=0.3)
    plt.legend(fontsize=9)

plt.tight_layout()
plt.savefig('car_gender_plot_4.png', dpi=150)
plt.show()
plt.close()

# -----------------------------------------------------------------------------------------
# [5] 연도별 연령대별 차량 등록 비중 (파이 차트) - 도시별 개별 그래프
print("\n[5] 연도별 연령대별 차량 등록 비중")

all_cities = ['Seoul', 'Busan', 'Daegu', 'Incheon', 'Gwangju', 'Ulsan']
all_years = [2020, 2021, 2022, 2023, 2024, 2025]

# 연령대별 색상 정의 (일관성을 위해)
age_colors = {
    '10대 이하': '#FF9999',
    '20대': '#66B2FF', 
    '30대': '#99FF99',
    '40대': '#FFCC99',
    '50대': '#FF99CC',
    '60대': '#99CCFF',
    '70대': '#FFD700',
    '80대': '#DDA0DD',
    '90대이상': '#F0E68C'
}

# 각 도시별로 개별 그래프 생성
for city in all_cities:
    city_name = city_map[city]
    
    # 2행 3열 그래프 (각 도시의 6개 연도)
    fig, axs = plt.subplots(2, 3, figsize=(13, 10))
    axs = axs.flatten()  # 2차원 배열을 1차원으로 평면화
    
    # 범례용 데이터 수집
    all_ages_in_city = set()
    
    for j, year in enumerate(all_years):
        # 해당 연도, 도시 데이터 가져오기
        df_slice = car_data[(car_data['Year'] == year) & (car_data['age'] != '계')]
        age_data = df_slice.groupby('age')[city].sum()
        
        # 0이 아닌 데이터만 사용
        age_data = age_data[age_data > 0]
        all_ages_in_city.update(age_data.index)
        
        if len(age_data) > 0:
            # 색상 매핑
            colors = [age_colors.get(age, '#CCCCCC') for age in age_data.index]
            
            # 파이 차트 그리기
            wedges, texts, autotexts = axs[j].pie(age_data.values, 
                                                 labels=age_data.index, 
                                                 colors=colors,
                                                 autopct='%1.0f%%',
                                                 startangle=90,
                                                 textprops={'fontsize': 20},  # 라벨 크기 축소
                                                 pctdistance=0.85)  # 퍼센트 텍스트 위치 조정
            
            # 퍼센트 텍스트 크기 조정
            for autotext in autotexts:
                autotext.set_fontsize(7)
                autotext.set_fontweight('bold')
            
            # 라벨 텍스트 크기 조정
            for text in texts:
                text.set_fontsize(8)
                
        else:
            axs[j].text(0.5, 0.5, '데이터\n없음', ha='center', va='center', fontsize=12)
        
        axs[j].set_title(f'{year}년', fontsize=14, fontweight='bold')
    
    # 범례 생성 (해당 도시에 존재하는 연령대만)
    legend_elements = []
    for age in age_order:  # 순서대로 표시
        if age in all_ages_in_city:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                            markerfacecolor=age_colors.get(age, '#CCCCCC'), 
                                            markersize=10, label=age))
    
    # 범례를 그래프 우측에 추가
    if legend_elements:
        fig.legend(handles=legend_elements, 
                  loc='center right', 
                  bbox_to_anchor=(0.98, 0.5),
                  fontsize=10)
    
    # 전체 제목 설정
    fig.suptitle(f'{city_name} 연도별 연령대별 차량 등록 비중', fontsize=16, y=0.98, fontweight='bold')
    
    plt.tight_layout()
    plt.subplots_adjust(right=0.85)  # 범례 공간 확보
    plt.savefig(f'car_gender_plot_5_{city_name}.png', dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()
    
    print(f'✓ {city_name} 그래프 저장 완료')

# -----------------------------------------------------------------------------------------
# [6] 연령별 성별 차량 등록수와 전체 등록수(total) 간 상관관계 분석
print("\n[7] 연령별 성별 차량 등록수와 전체 등록수(total) 간 상관관계 분석")

# '계' 제외
df_corr = car_data[car_data['age'] != '계']

# 결과 저장용 리스트
correlation_results = []

for age in age_order:
    for gender in ['남성', '여성']:
        temp_df = df_corr[(df_corr['age'] == age) & (df_corr['gender'] == gender)]
        
        if len(temp_df) >= 2:
            row = {
                '연령대': age,
                '성별': gender,
                '전체도시합 vs total': round(temp_df['total'].corr(temp_df[cities].sum(axis=1)), 4)
            }
            
            # 각 도시별로 상관계수 계산
            for city in cities:
                corr = temp_df['total'].corr(temp_df[city])
                row[f'{city} vs total'] = round(corr, 4)
            
            correlation_results.append(row)

# 데이터프레임으로 변환 및 출력
corr_df = pd.DataFrame(correlation_results)
print(tabulate(corr_df, headers='keys', tablefmt='psql'))

# -----------------------------------------------------------------------------------------
# [7] 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 히트맵용 데이터 변환
# 인덱스: 연령대 + 성별, 컬럼: 각 도시 vs total
heatmap_df = corr_df.copy()
heatmap_df['index'] = heatmap_df['연령대'] + ' (' + heatmap_df['성별'] + ')'
heatmap_df.set_index('index', inplace=True)

# 히트맵에 사용할 컬럼만 선택
columns_to_plot = [col for col in heatmap_df.columns if 'vs total' in col]
heatmap_data = heatmap_df[columns_to_plot]

# 히트맵 시각화
plt.figure(figsize=(14, 8))
sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, linecolor='gray', cbar=True)

plt.title('연령별 성별 차량 등록수와 전체 등록수 간 상관관계 히트맵', fontsize=14, fontweight='bold')
plt.ylabel('연령대 (성별)')
plt.xlabel('도시 vs Total')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('car_gender_plot_6_heatmap.png', dpi=150)
plt.show()

# [8] 주요 도시별 연도별 남녀 차량 등록현황 : 범위 조정
print("[1] 주요 도시별 연도별 남녀 차량 등록 현황")

plt.figure(figsize=(20, 10))

y_min_seoul = 100000
y_max_seoul = 2000000
y_ticks_seoul = [100000, 300000, 500000, 700000, 900000, 1100000, 1300000, 1500000, 1700000, 1900000, 2100000]

y_min_others = 100000
y_max_others = 800000
y_ticks_others = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000]

for i, city in enumerate(cities):
    city_name = city_map[city]

    male_data = car_data[(car_data['gender'] == '남성') & (car_data['age'] != '계')].groupby('Year')[city].sum()
    female_data = car_data[(car_data['gender'] == '여성') & (car_data['age'] != '계')].groupby('Year')[city].sum()

    plt.subplot(2, 3, i + 1)
    plt.plot(years, male_data, marker='o', label='남성', color='skyblue')
    plt.plot(years, female_data, marker='s', label='여성', color='lightcoral')

    plt.title(f'{city_name} 연도별 남녀 차량 등록', fontweight='bold')
    plt.xlabel('연도')
    plt.ylabel('등록 대수 (만 대)')
    plt.xticks(years)

    if city_name == '서울':
        plt.ylim(y_min_seoul, y_max_seoul)
        plt.yticks(y_ticks_seoul, [f'{int(tick / 10000)}' for tick in y_ticks_seoul])
    else:
        plt.ylim(y_min_others, y_max_others)
        plt.yticks(y_ticks_others, [f'{int(tick / 10000)}' for tick in y_ticks_others])

    plt.grid(True, alpha=0.3)
    plt.legend()

plt.tight_layout()
plt.savefig('car_gender_plot_1_modified.png', dpi=150)
plt.show()
plt.close()
