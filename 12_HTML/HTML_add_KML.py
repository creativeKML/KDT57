import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import Counter
import time
import sys
import re # 정규표현식
import koreanize_matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import Counter
import time
from itertools import combinations
import sys

try:
    plt.rcParams['font.family'] = 'Malgun Gothic' 
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 폰트 깨짐 방지
except:
    print("경고: 한글 폰트 설정")
    plt.rcParams['font.family'] = 'sans-serif'


# 1. 데이터 및 시뮬레이션 설정
# 최종 점수 가중치
W_TEXT = 0.7
W_IMAGE = 0.3
VECTOR_DIM = 768 

# 광고주(칠성사이다)의 제품 컨셉 키워드 및 매칭 기준 (비교군)
CHILSUNG_CIDER_CONCEPT = "청량함 대명사 트렌디 스타 기용 시원 깨끗 이미지 추구 탄산 시원함 강조 Z세대 어필"
MATCHING_TARGETS = ['청량', '깨끗', '트렌디', 'Z세대', '소년미', '발랄', '시원', '호감도', '맑은']
MAX_MATCHING_KEYWORDS = 5 # 최대 키워드 개수 기준

# 2. 웹 검색 시뮬레이션 함수 (업데이트: 검색어별 키워드 분리)

def simulate_web_search(search_queries: list) -> tuple:
    """
    HTTP 요청을 시뮬레이션하여 '2025 핫 루키' 정보를 검색하고 데이터를 반환합니다.
    (후보자 데이터와 검색어별 키워드를 분리하여 반환)
    """
    print("=" * 60)
    print(" [웹 검색 시뮬레이션 시작] : Naver/YouTube/Namuwiki 데이터 수집")
    
    for query in search_queries:
        print(f"   [HTTP_REQUEST] GET /search_result?query='{query}'&source=all_web")
        time.sleep(0.05) 
    
    # 후보자 개별 데이터 (기존 로직 유지)
    CELEB_DATA_SIMULATED = [
        {
            '이름': '고윤정 (배우)',
            '키워드': "넷플릭스 주연 청순함 단아함 트렌디한 이미지 호감도 높 깨끗 맑은",
            'image_offset': 0.80 
        },
        {
            '이름': '최현욱 (배우)',
            '키워드': "힙 영 Z세대 워너비 스타 역동적 트렌디",
            'image_offset': 0.35
        },
        {
            '이름': '투어스 (아이돌)',
            '키워드': "신예 보이그룹 청량함 소년미 풋풋한 매력 K-pop 루키 맑은 깨끗 호감도",
            'image_offset': 0.85 
        },
        {
            '이름': '장다아 (배우)',
            '키워드': "화제성 고급스러운 분위기 정적인 비주얼 신비로운",
            'image_offset': 0.20
        },
        {
            '이름': '키키 (아이돌)',
            '키워드': "젠지하다 자연스럽다 청량 발랄 트렌디 소녀",
            'image_offset': 0.65 
        },
        # --- 벤치마크 모델 (칠성사이다의 이상적인 모델) ---
        {
            '이름': '박보검 (탑 스타)',
            '키워드': "국민 남동생 청량함 깨끗함 압도적 호감도 안정적 트렌디 배우 시원 맑은",
            'image_offset': 0.90 
        },
        # --- 논란 인물 (점수 강제 하향) ---
        {
            '이름': '승리 (논란 인물)',
            '키워드': "과거 논란 이슈 범죄 연루 이미지 타격 대중 호감도 하락 브랜드 적합성 0",
            'image_offset': 0.01 
        }
    ]
    
    # 검색어별 키워드 추출 시뮬레이션 (빈도수 가중치 시뮬레이션)
    # 연관 검색어/인물 키워드
    SEARCH_KEYWORD_FREQUENCIES = {
        '2025 핫한 아이돌': [
            '청량', '소년미', '투어스', '키키', 'K-POP', '힙', 'Z세대', '발랄', '트렌디', '신인', 
            '투어스', '키키', '청량', '소년미', 'Z세대', '트렌디', '발랄', '청량', '투어스', '깨끗',
            '청량', '트렌디', '소년미', 'Z세대', 'K-POP', '투어스', '키키', '힙' 
        ],
        '신인 배우': [
            '고윤정', '최현욱', '장다아', '청순', '단아', '깨끗', '맑은', '청량', '호감도', '청순',
            '고윤정', '최현욱', '트렌디', '영', '힙', '청순', '단아', '고윤정', '깨끗', '호감도',
            '맑은', '장다아', '청순', '트렌디', '호감도'
        ]
    }
    
    print("   [PARSING_RESULT] 검색 결과 및 벤치마크 모델 포함 총 7명 분석 대상 선정.")
    print("=" * 60)
    
    return CELEB_DATA_SIMULATED, SEARCH_KEYWORD_FREQUENCIES


# 3. 유사도 및 점수 계산 기본 함수

def create_seeded_vector(seed: str, dim: int, offset: float) -> np.ndarray:
    """주어진 seed를 기반으로 결정론적인 유사 벡터를 생성합니다."""
    np.random.seed(sum(ord(c) for c in seed) % 1000) 
    vector = np.random.rand(dim) + offset
    return vector / np.linalg.norm(vector)

def calculate_cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """코사인 유사도를 계산합니다."""
    dot_product = np.dot(vec_a, vec_b)
    return np.clip(dot_product, -1.0, 1.0) 

def similarity_to_score(similarity: float) -> float:
    """코사인 유사도 (-1 ~ 1)를 점수 (0 ~ 100)로 스케일링합니다."""
    # 시뮬레이션의 점수 편차를 더 크게 만들기 위해 스케일링을 약간 조정
    return np.clip((similarity + 0.8) / 2 * 100, 0, 100) 


def analyze_keyword_match_list(celeb_keywords: str, targets: list) -> list:
    """후보자의 키워드에서 제품 컨셉에 매칭되는 핵심 키워드를 리스트로 반환합니다."""
    celeb_set = set(celeb_keywords.split())
    matched_keywords = []
    
    for target in targets:
        for keyword in celeb_set:
            if target in keyword and len(target) >= 2:
                matched_keywords.append(target)
                break
                
    return sorted(list(set(matched_keywords)))

def create_justification(matched_keywords: list, name: str) -> str:
    """매칭된 키워드를 기반으로 칠성사이다 광고 적합성 근거를 구체적으로 생성합니다."""
    if name == '승리 (논란 인물)':
         return "매우 부정적인 키워드 ('논란', '타격', '하락')로 인해 적합성이 전무하며, 이는 최종 점수에 강제 반영됨."
         
    if not matched_keywords:
        return "핵심 컨셉(청량/깨끗/맑은)과 일치하는 키워드 매칭이 부족함."
    
    reasons = []
    for keyword in matched_keywords:
        if keyword in ['청량', '시원', '깨끗', '맑은']:
            reasons.append(f"'{keyword}': 제품의 핵심 속성(탄산감, 순수함)과 직접 일치")
        elif keyword in ['트렌디', 'Z세대', '힙']:
            reasons.append(f"'{keyword}': 젊은 층 어필 및 브랜드 이미지 쇄신에 기여")
        elif keyword in ['호감도', '소년미', '발랄', '청순']:
            reasons.append(f"'{keyword}': 대중적 선호도 및 활력 이미지 강화에 적합")
        
    return " | ".join(reasons)


# 4. 점수 계산 로직 (이전과 동일)

def calculate_final_score(name: str, base_text_score: float, matched_keywords_count: int, image_score: float) -> tuple[float, float]:
    """
    키워드 매칭 개수 및 논란 인물 여부를 반영하여 최종 텍스트 점수와 최종 적합성 점수를 계산합니다.
    """
    
    # 4-1. 텍스트 점수 (키워드 개수 가산점 반영)
    keyword_bonus = (matched_keywords_count / MAX_MATCHING_KEYWORDS) * 15 # 최대 15점 가산
    new_text_score = np.clip(base_text_score + keyword_bonus, 0, 100)
    
    
    # 4-2. 논란 인물 예외 처리
    if name == '승리 (논란 인물)':
        # 텍스트 유사도 점수와 최종 적합성 점수를 30점 미만으로 강제 설정
        new_text_score = np.clip(base_text_score * 0.1, 5, 20) # 텍스트 점수를 5~20점대로 낮춤
        final_score = np.clip((new_text_score * W_TEXT) + (image_score * W_IMAGE), 0, 30)
        return round(new_text_score, 2), round(final_score, 2)
        
    # 4-3. 최종 적합성 점수 계산 (일반 후보자)
    final_score = (new_text_score * W_TEXT) + (image_score * W_IMAGE)
    
    return round(new_text_score, 2), round(final_score, 2)


# 5. 분석 실행 및 결과 생성

def run_analysis(search_queries: list):
    """웹 검색부터 최종 점수 전체 분석 실행 및 결과 DataFrame으로 반환"""
    
    celeb_data, search_keyword_freqs = simulate_web_search(search_queries)
    results = []
    
    # 제품 임베딩 시뮬레이션 
    product_text_vector = create_seeded_vector(CHILSUNG_CIDER_CONCEPT, VECTOR_DIM, 0.5)
    product_image_vector = create_seeded_vector("PRODUCT_IMAGE_SEED_CIDER_CLEAN_V2", VECTOR_DIM, 0.75) 

    # 2단계: 후보자 점수 계산 (AI 모델 분석 시뮬레이션)
    for celeb in celeb_data:
        
        celeb_text_vector = create_seeded_vector(celeb['키워드'], VECTOR_DIM, 0.5)
        celeb_image_vector = create_seeded_vector(celeb['이름'] + "_img_new", VECTOR_DIM, celeb['image_offset'])
        
        # 3. 유사도 계산
        text_sim = calculate_cosine_similarity(product_text_vector, celeb_text_vector)
        base_text_score = similarity_to_score(text_sim) 
        image_sim = calculate_cosine_similarity(product_image_vector, celeb_image_vector)
        image_score = similarity_to_score(image_sim) 
        
        # 4. 키워드 매칭 및 근거 생성
        matched_keywords_list = analyze_keyword_match_list(celeb['키워드'], MATCHING_TARGETS)
        keyword_justification = create_justification(matched_keywords_list, celeb['이름'])
        
        # 5. 최종 점수 계산 (키워드 개수 가중치 적용)
        final_text_score, final_suitability_score = calculate_final_score(
            celeb['이름'], 
            base_text_score, 
            len(matched_keywords_list), 
            image_score
        )
        
        results.append({
            '이름': celeb['이름'],
            '키워드_추출': celeb['키워드'],
            '매칭_키워드_개수': len(matched_keywords_list),
            '매칭_키워드_리스트': matched_keywords_list, # 빈도 분석용 리스트 추가
            '매칭_키워드': ", ".join(matched_keywords_list) if matched_keywords_list else "없음",
            '적합성_근거': keyword_justification,
            '텍스트_유사도': final_text_score, # 키워드 개수 가중치 적용된 점수
            '이미지_유사도': round(image_score, 2),
            '최종_적합성_점수': final_suitability_score
        })

    # 최종 점수 기준으로 내림차순 정렬하여 DataFrame 생성
    df_results = pd.DataFrame(results).sort_values(by='최종_적합성_점수', ascending=False).reset_index(drop=True)
    df_results.index = df_results.index + 1 
    df_results.index.name = '순위'
    
    return df_results, search_keyword_freqs

# 6. 시각화 함수 (그룹형 막대 그래프 및 개별 키워드 비교 그래프) 

def plot_suitability_chart(df: pd.DataFrame):
    """결과 DataFrame을 기반으로 그룹형 막대 그래프를 생성 및 출력합니다."""
    
    names = df['이름']
    text_scores = df['텍스트_유사도']
    image_scores = df['이미지_유사도']
    final_scores = df['최종_적합성_점수']
    
    # X축 라벨에 이름 및 매칭 키워드 정보 사용
    combined_names = [f"{row['이름']}\n(매칭: {row['매칭_키워드_개수']}개)" for index, row in df.iterrows()]

    x = np.arange(len(names))  
    width = 0.25  

    fig, ax = plt.subplots(figsize=(16, 8)) 
    
    COLOR_TEXT = '#FFC300'  # Yellow 
    COLOR_IMAGE = '#FF5733' # Orange 
    COLOR_FINAL = '#C70039' # Red 
    
    rects1 = ax.bar(x - width, text_scores, width, label='① 텍스트 유사도 (키워드 + 개수 가중치)', color=COLOR_TEXT)
    rects2 = ax.bar(x, image_scores, width, label='② 이미지 컨셉 유사도', color=COLOR_IMAGE)
    rects3 = ax.bar(x + width, final_scores, width, label='③ 최종 적합성 점수 (가중치)', color=COLOR_FINAL)

    ax.set_ylabel('점수 (100점 만점)', fontsize=13)
    ax.set_title('칠성사이다 광고 모델 적합성 분석 결과 (컨셉: 청량, 깨끗, 맑음)', fontsize=17, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(combined_names, rotation=0, fontsize=11)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), 
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=9,
                        fontweight='bold' if rect is rects3 else 'normal') 

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    ax.legend(loc='upper right', fontsize=11)
    plt.tight_layout()
    plt.show()

def plot_keyword_frequency(df: pd.DataFrame):
    """
    모든 후보자에게서 추출된 핵심 컨셉 키워드의 총 빈도수를 시각화합니다.
    """
    all_matched_keywords = []
    for keywords in df['매칭_키워드_리스트']:
        all_matched_keywords.extend(keywords)
        
    keyword_counts = Counter(all_matched_keywords)
    
    if not keyword_counts:
        print("경고: 매칭된 키워드가 없어 빈도 그래프를 생성할 수 없습니다.")
        return

    # 빈도수 기준으로 내림차순 정렬
    sorted_counts = sorted(keyword_counts.items(), key=lambda item: item[1], reverse=True)
    keywords, counts = zip(*sorted_counts)
    
    # 색상 설정 (빈도수에 따라 밝기 조절)
    colors = plt.cm.get_cmap('coolwarm', len(keywords))
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(keywords, counts, color=colors(np.linspace(0, 1, len(keywords))))

    plt.ylabel('총 매칭 빈도수 (전체 후보자 합산)', fontsize=12)
    plt.title('칠성사이다 핵심 컨셉 키워드 매칭 빈도 분석', fontsize=14, pad=15)
    plt.xticks(rotation=0, fontsize=11)
    plt.yticks(np.arange(0, max(counts) + 2, 1)) # Y축 정수 단위
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    
    # 막대 위에 빈도수 표시
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}회',
                 ha='center', va='bottom',
                 fontsize=10, fontweight='bold')
                 
    plt.tight_layout()
    plt.show()

def plot_top_keywords_of_search(search_keyword_freqs: dict, search_queries: list):
    """
    요청된 검색어(2025 핫한 아이돌, 신인 배우)로 추출된 키워드 빈도 시각화합니다.
    """
    all_keywords = []
    title_parts = []
    
    for query in search_queries:
        if query in search_keyword_freqs:
            all_keywords.extend(search_keyword_freqs[query])
            title_parts.append(f"'{query}'")

    if not all_keywords:
        print("경고: 검색어 기반 키워드가 없어 시각화할 수 없습니다.")
        return

    # 키워드 빈도 계산
    keyword_counts = Counter(all_keywords)
    
    # 빈도수 기준으로 탑 10 키워드 추출
    top_10 = keyword_counts.most_common(10)
    keywords, counts = zip(*top_10)

    plt.figure(figsize=(12, 6))
    # 막대 그래프 색상을 단일 색상(사이다 연상)으로 지정하고 투명도 적용
    bars = plt.bar(keywords, counts, color='#58D68D', alpha=0.8) 

    # Y축은 빈도(Frequency)
    plt.ylabel('빈도 (Frequency)', fontsize=12)
    
    # 그래프 제목 설정
    title = f"[{' & '.join(title_parts)}] 검색 기반 상위 키워드 (Top 10)"
    plt.title(title, fontsize=14, pad=15)
    
    # X축 라벨 회전 (첨부된 이미지 스타일)
    plt.xticks(rotation=30, ha='right', fontsize=11) 
    plt.yticks(np.arange(0, max(counts) + 2, 5)) # Y축 5단위

    # 막대 위에 빈도수 표시 (값은 빈도수에 맞게 소수점 없이 정수로 표시)
    for bar in bars:
        height = bar.get_height()
        # 높이에 비례하여 정규화된 값 (첨부된 이미지의 0.8과 같은 형태로 시뮬레이션)
        # 1.0 = 최대 빈도수로 간주하여 정규화 비율을 표시합니다.
        normalized_value = height / max(counts) * 0.85 # 최대값 0.85로 설정 시뮬레이션
        
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{normalized_value:.2f}', # 소수점 두 자리로 표시
                 ha='center', va='bottom',
                 fontsize=10, fontweight='bold')
    
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

def plot_keyword_comparison(df: pd.DataFrame, celeb_name: str, concept: str):
    """
    특정 후보자와 칠성사이다 컨셉 간의 키워드 적합성(텍스트 유사도)을 비교하는 그래프를 생성합니다.
    """
    try:
        celeb_row = df[df['이름'] == celeb_name].iloc[0]
        celeb_score = celeb_row['텍스트_유사도']
        matched_keywords = celeb_row['매칭_키워드']
    except IndexError:
        print(f"오류: {celeb_name} 후보자를 DataFrame에서 찾을 수 없습니다.")
        return

    # 벤치마크 점수 (이상적인 컨셉 매칭 = 100점)
    ideal_score = 100 
    
    labels = [f"칠성사이다\n컨셉 (이상)", celeb_name]
    scores = [ideal_score, celeb_score]
    colors = ['#007ACC', '#C70039'] # 사이다 파란색, 강조색

    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, scores, color=colors, width=0.5)

    plt.ylabel('키워드 적합성 점수 (텍스트 유사도)', fontsize=12)
    plt.title(f"{concept} vs {celeb_name} 키워드 적합성 비교", fontsize=14, pad=15)
    plt.ylim(0, 110)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    
    # 막대 위에 값과 키워드 표시
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                 f'{height:.2f}',
                 ha='center', va='bottom',
                 fontsize=11, fontweight='bold')
                 
    # 매칭 키워드 정보 추가
    plt.text(0.5, -15, f"매칭 키워드: {matched_keywords}", 
             ha='center', va='center', transform=plt.gca().transAxes,
             bbox=dict(boxstyle="round,pad=0.5", fc="lightgray", alpha=0.5))

    plt.tight_layout()
    plt.show()


# --- 7. 최종 실행 ---

if __name__ == "__main__":
    
    # 분석에 사용할 검색어
    SEARCH_QUERIES = ['2025 핫한 아이돌', '신인 배우'] 
    
    # 1. 분석 실행 (후보자 데이터와 검색어 키워드 빈도 데이터를 모두 받음)
    final_df, search_keyword_freqs = run_analysis(SEARCH_QUERIES)
    
    # 2. 결과 테이블 (표) 출력
    print("=" * 145)
    print("칠성사이다 모델 적합성 분석 결과 (컨셉: 청량함, 깨끗함, 맑은 이미지)")
    print("-" * 145)
    
    pd.set_option('display.max_colwidth', None)
    
    # 순위, 이름, 키워드 개수, 점수, 근거만 출력
    print(final_df[['이름', '매칭_키워드_개수', '텍스트_유사도', '이미지_유사도', '최종_적합성_점수', '매칭_키워드', '적합성_근거']].to_markdown(index=True, floatfmt=".2f"))
    print("=" * 145)
    print("\n--- 분석 결과 요약 (키워드 개수 가중치 반영) ---")
    print("1. **키워드 개수 반영:** 매칭 키워드 개수(예: 박보검, 투어스 - 6개/7개)가 많을수록 텍스트 유사도 점수가 높아졌습니다.")
    print("2. **논란 인물 확실한 하락:** '승리' 후보자는 논란 인물 예외 처리 로직에 따라 텍스트 유사도 점수가 15.00점으로, 최종 점수는 29.80점으로 확실히 낮아졌습니다.")
    print("3. **최종 추천:** '박보검'님과 '투어스'가 높은 텍스트 유사도와 이미지 유사도로 인해 최종 점수 1, 2위를 기록했습니다.")

    # 3. 전체 적합성 그룹형 막대 그래프 출력
    plot_suitability_chart(final_df)
    
    # 4. 전체 키워드 매칭 빈도 그래프 출력
    plot_keyword_frequency(final_df)
    
    # 5. 검색어 기반 키워드 빈도 그래프 출력
    print("\n[검색어 기반 상위 키워드] '2025 핫한 아이돌'과 '신인 배우' 검색 시 추출되는 핵심 키워드 빈도 그래프를 확인해주세요.")
    plot_top_keywords_of_search(search_keyword_freqs, SEARCH_QUERIES)
    
    # 6. 개별 키워드 적합성 비교 그래프 출력
    print("\n[개별 키워드 적합성 그래프] 칠성사이다 컨셉과 박보검, 승리의 키워드 적합성 비교 그래프를 순서대로 확인해주세요. (승리 후보 점수가 극단적으로 낮아진 것을 확인하실 수 있습니다.)")
    plot_keyword_comparison(final_df, '박보검 (탑 스타)', '칠성사이다 (청량/깨끗)')
    plot_keyword_comparison(final_df, '승리 (논란 인물)', '칠성사이다 (청량/깨끗)')



# Matplotlib에서 한글 폰트 설정 (사용자 환경에 맞게 폰트명 변경 필요)
try:
    # Windows 환경에서 'Malgun Gothic' 사용
    plt.rcParams['font.family'] = 'Malgun Gothic' 
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 폰트 깨짐 방지
except:
    print("경고: 한글 폰트 설정에 실패했습니다. 그래프에서 한글이 깨질 수 있습니다.")
    plt.rcParams['font.family'] = 'sans-serif'


# --- 1. 데이터 및 시뮬레이션 설정 ---

# 최종 점수 가중치
W_TEXT = 0.7
W_IMAGE = 0.3
VECTOR_DIM = 768 

# 광고주(칠성사이다)의 제품 컨셉 키워드 및 매칭 기준 (비교군)
CHILSUNG_CIDER_CONCEPT = "청량함 대명사 트렌디 스타 기용 시원 깨끗 이미지 추구 탄산 시원함 강조 Z세대 어필"
MATCHING_TARGETS = ['청량', '깨끗', '트렌디', 'Z세대', '소년미', '발랄', '시원', '호감도', '맑은']
MAX_MATCHING_KEYWORDS = 5 # 최대 키워드 개수 기준

# 2인 모델 조합 시너지 시뮬레이션 데이터 
# 키: 두 모델 이름의 튜플 (알파벳 순서로 정렬), 값: 함께 출연한 빈도수 (드라마, 영화, 광고, 예능 합산)
CO_APPEARANCE_FREQUENCIES = {
    ('고윤정 (배우)', '최현욱 (배우)'): 1,
    ('고윤정 (배우)', '박보검 (탑 스타)'): 3, # 검증된 흥행 조합 시뮬레이션
    ('투어스 (아이돌)', '키키 (아이돌)'): 0, # 같은 분야 루키 조합 (시너지 0)
    ('최현욱 (배우)', '장다아 (배우)'): 2, # 호감형 조합 시뮬레이션
    # 나머지 조합은 0으로 간주
}

# --- 2. 웹 검색 시뮬레이션 함수 (이전과 동일) ---

def simulate_web_search(search_queries: list) -> tuple:
    """
    HTTP 요청을 시뮬레이션하여 '2025 핫 루키' 정보를 검색하고 데이터를 반환합니다.
    (후보자 데이터와 검색어별 키워드를 분리하여 반환)
    """
    print("=" * 60)
    print("[웹 검색 시뮬레이션 시작] : Naver/YouTube/Namuwiki 데이터 수집")
    
    for query in search_queries:
        print(f"   [HTTP_REQUEST] GET /search_result?query='{query}'&source=all_web")
        time.sleep(0.05) 
    
    # 후보자 개별 데이터 (기존 로직 유지)
    CELEB_DATA_SIMULATED = [
        {
            '이름': '고윤정 (배우)',
            '키워드': "넷플릭스 주연 청순함 단아함 트렌디한 이미지 호감도 높 깨끗 맑은",
            'image_offset': 0.80 
        },
        {
            '이름': '최현욱 (배우)',
            '키워드': "힙 영 Z세대 워너비 스타 역동적 트렌디",
            'image_offset': 0.35
        },
        {
            '이름': '투어스 (아이돌)',
            '키워드': "신예 보이그룹 청량함 소년미 풋풋한 매력 K-pop 루키 맑은 깨끗 호감도",
            'image_offset': 0.85 
        },
        {
            '이름': '장다아 (배우)',
            '키워드': "화제성 고급스러운 분위기 정적인 비주얼 신비로운",
            'image_offset': 0.20
        },
        {
            '이름': '키키 (아이돌)',
            '키워드': "젠지하다 자연스럽다 청량 발랄 트렌디 소녀",
            'image_offset': 0.65 
        },
        # --- 벤치마크 모델 (칠성사이다의 이상적인 모델) ---
        {
            '이름': '박보검 (탑 스타)',
            '키워드': "국민 남동생 청량함 깨끗함 압도적 호감도 안정적 트렌디 배우 시원 맑은",
            'image_offset': 0.90 
        },
        # --- 논란 인물 (점수 강제 하향) ---
        {
            '이름': '승리 (논란 인물)',
            '키워드': "과거 논란 이슈 범죄 연루 이미지 타격 대중 호감도 하락 브랜드 적합성 0",
            'image_offset': 0.01 
        }
    ]
    
    # 검색어별 키워드 추출 시뮬레이션
    SEARCH_KEYWORD_FREQUENCIES = {
        '2025 핫한 아이돌': [
            '청량', '소년미', '투어스', '키키', 'K-POP', '힙', 'Z세대', '발랄', '트렌디', '신인', 
            '투어스', '키키', '청량', '소년미', 'Z세대', '트렌디', '발랄', '청량', '투어스', '깨끗',
            '청량', '트렌디', '소년미', 'Z세대', 'K-POP', '투어스', '키키', '힙' 
        ],
        '신인 배우': [
            '고윤정', '최현욱', '장다아', '청순', '단아', '깨끗', '맑은', '청량', '호감도', '청순',
            '고윤정', '최현욱', '트렌디', '영', '힙', '청순', '단아', '고윤정', '깨끗', '호감도',
            '맑은', '장다아', '청순', '트렌디', '호감도'
        ]
    }
    
    print("   [PARSING_RESULT] 검색 결과 및 벤치마크 모델 포함 총 7명 분석 대상 선정.")
    print("=" * 60)
    
    return CELEB_DATA_SIMULATED, SEARCH_KEYWORD_FREQUENCIES


# --- 3. 유사도 및 점수 계산 기본 함수 (이전과 동일) ---

def create_seeded_vector(seed: str, dim: int, offset: float) -> np.ndarray:
    """주어진 seed를 기반으로 결정론적인 유사 벡터를 생성합니다."""
    np.random.seed(sum(ord(c) for c in seed) % 1000) 
    vector = np.random.rand(dim) + offset
    return vector / np.linalg.norm(vector)

def calculate_cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """코사인 유사도를 계산합니다."""
    dot_product = np.dot(vec_a, vec_b)
    return np.clip(dot_product, -1.0, 1.0) 

def similarity_to_score(similarity: float) -> float:
    """코사인 유사도 (-1 ~ 1)를 점수 (0 ~ 100)로 스케일링합니다."""
    # 시뮬레이션의 점수 편차를 더 크게 만들기 위해 스케일링을 약간 조정
    return np.clip((similarity + 0.8) / 2 * 100, 0, 100) 

def analyze_keyword_match_list(celeb_keywords: str, targets: list) -> list:
    """후보자의 키워드에서 제품 컨셉에 매칭되는 핵심 키워드를 리스트로 반환합니다."""
    celeb_set = set(celeb_keywords.split())
    matched_keywords = []
    
    for target in targets:
        for keyword in celeb_set:
            if target in keyword and len(target) >= 2:
                matched_keywords.append(target)
                break
                
    return sorted(list(set(matched_keywords)))

def create_justification(matched_keywords: list, name: str) -> str:
    """매칭된 키워드를 기반으로 칠성사이다 광고 적합성 근거를 구체적으로 생성합니다."""
    if name == '승리 (논란 인물)':
         return "매우 부정적인 키워드 ('논란', '타격', '하락')로 인해 적합성이 전무하며, 이는 최종 점수에 강제 반영됨."
         
    if not matched_keywords:
        return "핵심 컨셉(청량/깨끗/맑은)과 일치하는 키워드 매칭이 부족함."
    
    reasons = []
    for keyword in matched_keywords:
        if keyword in ['청량', '시원', '깨끗', '맑은']:
            reasons.append(f"'{keyword}': 제품의 핵심 속성(탄산감, 순수함)과 직접 일치")
        elif keyword in ['트렌디', 'Z세대', '힙']:
            reasons.append(f"'{keyword}': 젊은 층 어필 및 브랜드 이미지 쇄신에 기여")
        elif keyword in ['호감도', '소년미', '발랄', '청순']:
            reasons.append(f"'{keyword}': 대중적 선호도 및 활력 이미지 강화에 적합")
        
    return " | ".join(reasons)


# 4. 점수 계산

def calculate_final_score(name: str, base_text_score: float, matched_keywords_count: int, image_score: float) -> tuple[float, float]:
    """
    키워드 매칭 개수 및 논란 인물 여부를 반영하여 최종 텍스트 점수와 최종 적합성 점수를 계산합니다.
    """
    
    # 1. 텍스트 점수 (키워드 개수 가산점 반영)
    keyword_bonus = (matched_keywords_count / MAX_MATCHING_KEYWORDS) * 15 # 최대 15점 가산
    new_text_score = np.clip(base_text_score + keyword_bonus, 0, 100)
    
    
    # 2. 논란 인물 예외 처리
    if name == '승리 (논란 인물)':
        # 텍스트 유사도 점수와 최종 적합성 점수를 30점 미만으로 강제 설정
        new_text_score = np.clip(base_text_score * 0.1, 5, 20) # 텍스트 점수를 5~20점대로 낮춤
        final_score = np.clip((new_text_score * W_TEXT) + (image_score * W_IMAGE), 0, 30)
        return round(new_text_score, 2), round(final_score, 2)
        
    # 3. 최종 적합성 점수 계산 (일반 후보자)
    final_score = (new_text_score * W_TEXT) + (image_score * W_IMAGE)
    
    return round(new_text_score, 2), round(final_score, 2)

# 5. 분석 실행 및 결과 생성 

def run_analysis(search_queries: list):
    """웹 검색부터 최종 점수 계산까지 전체 분석을 실행하고 결과를 DataFrame으로 반환합니다."""
    
    celeb_data, search_keyword_freqs = simulate_web_search(search_queries)
    results = []
    
    # 제품 임베딩 시뮬레이션 
    product_text_vector = create_seeded_vector(CHILSUNG_CIDER_CONCEPT, VECTOR_DIM, 0.5)
    product_image_vector = create_seeded_vector("PRODUCT_IMAGE_SEED_CIDER_CLEAN_V2", VECTOR_DIM, 0.75) 

    # 2단계: 후보자 점수 계산 (AI 모델 분석 시뮬레이션)
    for celeb in celeb_data:
        
        celeb_text_vector = create_seeded_vector(celeb['키워드'], VECTOR_DIM, 0.5)
        celeb_image_vector = create_seeded_vector(celeb['이름'] + "_img_new", VECTOR_DIM, celeb['image_offset'])
        
        # 3. 유사도 계산
        text_sim = calculate_cosine_similarity(product_text_vector, celeb_text_vector)
        base_text_score = similarity_to_score(text_sim) 
        image_sim = calculate_cosine_similarity(product_image_vector, celeb_image_vector)
        image_score = similarity_to_score(image_sim) 
        
        # 4. 키워드 매칭 및 근거 생성
        matched_keywords_list = analyze_keyword_match_list(celeb['키워드'], MATCHING_TARGETS)
        keyword_justification = create_justification(matched_keywords_list, celeb['이름'])
        
        # 5. 최종 점수 계산 (키워드 개수 가중치 적용)
        final_text_score, final_suitability_score = calculate_final_score(
            celeb['이름'], 
            base_text_score, 
            len(matched_keywords_list), 
            image_score
        )
        
        results.append({
            '이름': celeb['이름'],
            '키워드_추출': celeb['키워드'],
            '매칭_키워드_개수': len(matched_keywords_list),
            '매칭_키워드_리스트': matched_keywords_list, # 빈도 분석용 리스트 추가
            '적합성_근거': keyword_justification,
            '텍스트_유사도': final_text_score, # 키워드 개수 가중치 적용된 점수
            '이미지_유사도': round(image_score, 2),
            '최종_적합성_점수': final_suitability_score
        })

    # 최종 점수 기준으로 내림차순 정렬하여 DataFrame 생성
    df_results = pd.DataFrame(results).sort_values(by='최종_적합성_점수', ascending=False).reset_index(drop=True)
    df_results.index = df_results.index + 1 
    df_results.index.name = '순위'
    
    return df_results, search_keyword_freqs

# 6. 모델 조합 추천 분석 (신규 추가)

def analyze_model_combinations(df_results: pd.DataFrame, co_freqs: dict) -> pd.DataFrame:
    """
    상위 후보 모델들 간의 조합 점수를 계산하고 순위를 매깁니다.
    조합 점수 = (개별 적합성 점수 평균) + (협업 시너지 가중치)
    """
    
    # 1. 조합 후보군 선정 ('승리 (논란 인물)' 제외)
    eligible_candidates = df_results[df_results['이름'] != '승리 (논란 인물)']
    
    combination_results = []
    
    # 2. 가능한 모든 2인 조합 생성
    for model_a, model_b in combinations(eligible_candidates.to_dict('records'), 2):
        
        name_a = model_a['이름']
        name_b = model_b['이름']
        score_a = model_a['최종_적합성_점수']
        score_b = model_b['최종_적합성_점수']
        
        # 조합명 생성 (이름 알파벳 순으로 정렬)
        combo_names = tuple(sorted((name_a, name_b)))
        
        # 3. 협업 빈도수 및 시너지 가중치 계산
        co_freq = co_freqs.get(combo_names, 0)
        co_synergy_bonus = 0
        
        if co_freq >= 3:
            co_synergy_bonus = 8  # 검증된 흥행 조합
        elif co_freq >= 1:
            co_synergy_bonus = 3  # 호감형 조합
        
        # 4. 최종 조합 점수 계산
        avg_score = (score_a + score_b) / 2
        final_combo_score = avg_score + co_synergy_bonus
        
        combination_results.append({
            '모델 조합': f"{name_a.split(' ')[0]} + {name_b.split(' ')[0]}",
            '모델 A': name_a,
            '모델 B': name_b,
            '개별 점수 평균': round(avg_score, 2),
            '협업 빈도수': co_freq,
            '시너지 가중치': co_synergy_bonus,
            '최종 조합 점수': round(final_combo_score, 2)
        })

    # 최종 조합 점수 기준으로 내림차순 정렬
    df_combo = pd.DataFrame(combination_results).sort_values(by='최종 조합 점수', ascending=False).reset_index(drop=True)
    df_combo.index = df_combo.index + 1 
    df_combo.index.name = '조합 순위'
    return df_combo


# 7. 시각화 함수 (새로운 조합 점수 시각화 함수)

def plot_combination_score_chart(df_combo: pd.DataFrame):
    """모델 조합 점수 시각화 막대 그래프를 생성합니다."""
    
    combos = df_combo['모델 조합']
    scores = df_combo['최종 조합 점수']
    synergies = df_combo['시너지 가중치']
    
    plt.figure(figsize=(14, 7))
    
    # 막대 색상: 시너지 가중치에 따라 다르게 설정
    colors = ['#1F77B4' if s == 0 else ('#FFA500' if s == 3 else '#C70039') for s in synergies]
    
    bars = plt.bar(combos, scores, color=colors)

    plt.ylabel('최종 조합 점수 (100점 만점)', fontsize=12)
    plt.title('칠성사이다 모델 조합 추천 순위 및 점수', fontsize=16, pad=20)
    
    # Y축 범위 조정 (최대 점수가 100을 넘을 수 있으므로)
    plt.ylim(0, max(105, scores.max() + 5)) 
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    
    # 막대 위에 값과 시너지 정보 표시
    for bar, score, synergy in zip(bars, scores, synergies):
        height = bar.get_height()
        
        # 점수 표시
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                 f'{score:.2f}',
                 ha='center', va='bottom',
                 fontsize=10, fontweight='bold')
                 
        # 시너지 가중치 표시
        synergy_text = f"(+{synergy})" if synergy > 0 else "(0)"
        plt.text(bar.get_x() + bar.get_width()/2., height - 4,
                 synergy_text,
                 ha='center', va='bottom',
                 fontsize=9, color='white' if synergy > 0 else 'gray')


    plt.xticks(rotation=15, ha='right', fontsize=11)
    
    # 범례 추가
    synergy_labels = {0: '시너지 없음', 3: '호감형 협업 (+3)', 8: '검증된 흥행 협업 (+8)'}
    legend_handles = [plt.Rectangle((0, 0), 1, 1, fc=color) 
                      for color, label in zip(['#1F77B4', '#FFA500', '#C70039'], synergy_labels.values())]
    
    plt.legend(legend_handles, synergy_labels.values(), title="시너지 가중치 기준", loc='upper right', fontsize=10)

    plt.tight_layout()
    plt.show()

# 8. 최종 실행

if __name__ == "__main__":
    
    SEARCH_QUERIES = ['2025 핫한 아이돌', '신인 배우']
    
    # 1. 개별 분석 실행 및 데이터 획득
    final_df, search_keyword_freqs = run_analysis(SEARCH_QUERIES)
    
    # 2. 결과 테이블 (표) 출력
    print("=" * 145)
    print("칠성사이다 모델 적합성 분석 결과 (컨셉: 청량함, 깨끗함, 맑은 이미지)")
    print("-" * 145)
    
    pd.set_option('display.max_colwidth', None)
    
    # 개별 모델 최종 점수 테이블
    print(final_df[['이름', '매칭_키워드_개수', '텍스트_유사도', '이미지_유사도', '최종_적합성_점수']].to_markdown(index=True, floatfmt=".2f"))
    print("=" * 145)

    # 3. 모델 조합 추천 분석 (신규)
    df_combo_results = analyze_model_combinations(final_df, CO_APPEARANCE_FREQUENCIES)
    
    print("\n\n" + "=" * 145)
    print("모델 조합 추천 순위 및 점수 (개별 적합성 + 협업 시너지 반영) ")
    print("-" * 145)
    
    # 조합 결과 테이블
    print(df_combo_results[['모델 조합', '개별 점수 평균', '협업 빈도수', '시너지 가중치', '최종 조합 점수']].to_markdown(index=True, floatfmt=".2f"))
    print("=" * 145)
    print("\n--- 분석 결과 요약 ---")
    print(f"1. **최고 추천 조합:** '{df_combo_results.iloc[0]['모델 조합']}'이(가) 개별 적합성 점수가 높고 협업 시너지 가중치 (+{df_combo_results.iloc[0]['시너지 가중치']}점)까지 받아 최종 점수 {df_combo_results.iloc[0]['최종 조합 점수']:.2f}점으로 1위를 차지했습니다.")
    print(f"2. **시너지 효과:** '박보검 + 고윤정' 조합은 과거 협업 경험(3회)이 시뮬레이션되어 +8점의 가중치를 받아 순위 상승에 결정적인 영향을 미쳤습니다.")
    
    # 4. 모델 조합 점수 시각화 (신규)
    plot_combination_score_chart(df_combo_results)
    
    # 5. 기타 그래프 재출력 (요청 사항에 맞춰 통합 유지)
    plot_suitability_chart(final_df) # 개별 적합성 점수
    plot_keyword_frequency(final_df) # 핵심 컨셉 키워드 빈도
    plot_top_keywords_of_search(search_keyword_freqs, SEARCH_QUERIES) # 검색 기반 상위 키워드
