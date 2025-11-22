# =========================================================
#  A. 복지 워드클라우드 (Selenium으로 복지 탭 정확 위치 크롤링)
#  B. 그룹별 평균연봉(막대) + 평점(꺾은선) [CSV: ./jobplanet_company_300.csv]
# 산출물: ./benefit_outputs 폴더에 이미지/CSV 저장
# =========================================================

import os, re, time, platform
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from wordcloud import WordCloud

# ---------- 시각화 ----------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Windows':
    FONT_PATH = r'c:\windows\Fonts\malgun.ttf'
elif platform.system() == 'Darwin':
    FONT_PATH = r'/System/Library/Fonts/AppleGothic.ttf'
else:
    FONT_PATH = r'/usr/share/fonts/truetype/nanum/NanumGothic.ttf'

os.makedirs("./benefit_outputs", exist_ok=True)
# =========================================================
# A) 복지 워드클라우드 (정확 위치)
#    - 위치: #welfare-item-list > div > div > ul > li > div
#      * h5.welfare-bullet__tit (카테고리)
#      * ul.welfare-bullet__list > li (키워드)
# =========================================================

# --- 그룹별 회사 URL 맵 (기업명 리스트) ---
seoul_big_company_benefits_url_map = {
    "두나무(주)" : "https://www.jobplanet.co.kr/companies/308146/reviews/%EB%91%90%EB%82%98%EB%AC%B4?",
    "(주)넥슨게임즈" : "https://www.jobplanet.co.kr/companies/392405/reviews/%EB%84%A5%EC%8A%A8%EA%B2%8C%EC%9E%84%EC%A6%88?",
    "SK텔레콤(주)" : "https://www.jobplanet.co.kr/companies/20575/reviews/sk%ED%85%94%EB%A0%88%EC%BD%A4?",
    "에스에이피코리아(주)" : "https://www.jobplanet.co.kr/companies/20860/reviews/%EC%97%90%EC%8A%A4%EC%97%90%EC%9D%B4%ED%94%BC%EC%BD%94%EB%A6%AC%EC%95%84?",
    "우리에프아이에스(주)" : "https://www.jobplanet.co.kr/companies/16738/reviews/%EC%9A%B0%EB%A6%AC%EC%97%90%ED%94%84%EC%95%84%EC%9D%B4%EC%97%90%EC%8A%A4?",
    "(주)코스콤" : "https://www.jobplanet.co.kr/companies/52769/reviews/%EC%BD%94%EC%8A%A4%EC%BD%A4?",
    "나이스정보통신(주)" : "https://www.jobplanet.co.kr/companies/42729/reviews/%EB%82%98%EC%9D%B4%EC%8A%A4%EC%A0%95%EB%B3%B4%ED%86%B5%EC%8B%A0?",
    "(주)쿠팡페이" : "https://www.jobplanet.co.kr/companies/372355/reviews/%EC%BF%A0%ED%8C%A1%ED%8E%98%EC%9D%B4?",
    "(주)메디플러스솔루션" : "https://www.jobplanet.co.kr/companies/327696/reviews/%EB%A9%94%EB%94%94%ED%94%8C%EB%9F%AC%EC%8A%A4%EC%86%94%EB%A3%A8%EC%85%98?",
    "(주)지마켓" : "https://www.jobplanet.co.kr/companies/58985/reviews/%EC%A7%80%EB%A7%88%EC%BC%93?"
}
seoul_frorein_company_benefits_url_map = {
    "페이스북코리아(유)" : "https://www.jobplanet.co.kr/companies/90364/reviews/%ED%8E%98%EC%9D%B4%EC%8A%A4%EB%B6%81%EC%BD%94%EB%A6%AC%EC%95%84?",
    "(유)로지텍코리아" : "https://www.jobplanet.co.kr/companies/86581/reviews/%EB%A1%9C%EC%A7%80%ED%85%8D%EC%BD%94%EB%A6%AC%EC%95%84?",
    "유니티테크놀로지스코리아(유)" : "https://www.jobplanet.co.kr/companies/94877/reviews/%EC%9C%A0%EB%8B%88%ED%8B%B0%ED%85%8C%ED%81%AC%EB%86%80%EB%A1%9C%EC%A7%80%EC%8A%A4%EC%BD%94%EB%A6%AC%EC%95%84?",
    "(주)벡터코리아아이티" : "https://www.jobplanet.co.kr/companies/75756/reviews/%EB%B2%A1%ED%84%B0%EC%BD%94%EB%A6%AC%EC%95%84%EC%95%84%EC%9D%B4%ED%8B%B0?",
    "(유)일루미나리안" : "https://www.jobplanet.co.kr/companies/345669/reviews/%EC%9D%BC%EB%A3%A8%EB%AF%B8%EB%82%98%EB%A6%AC%EC%95%88?",
    "(유)프리디소프트" : "https://www.jobplanet.co.kr/companies/328375/reviews/%ED%94%84%EB%A6%AC%EB%94%94%EC%86%8C%ED%94%84%ED%8A%B8?",
    "브이엠웨어코리아(유)" : "https://www.jobplanet.co.kr/companies/311177/reviews/%EB%B8%8C%EC%9D%B4%EC%97%A0%EC%9B%A8%EC%96%B4%EC%BD%94%EB%A6%AC%EC%95%84?",
    "앱리프트아시아퍼시픽(주)" : "https://www.jobplanet.co.kr/companies/96767/reviews/%EC%95%B1%EB%A6%AC%ED%94%84%ED%8A%B8%EC%95%84%EC%8B%9C%EC%95%84%ED%8D%BC%EC%8B%9C%ED%94%BD?",
    "일렉트로닉아츠코리아(유)" : "https://www.jobplanet.co.kr/companies/12945/reviews/%EC%9D%BC%EB%A0%89%ED%8A%B8%EB%A1%9C%EB%8B%89%EC%95%84%EC%B8%A0%EC%BD%94%EB%A6%AC%EC%95%84?",
    "비바시스템즈코리아(유)" : "https://www.jobplanet.co.kr/companies/345849/reviews/%EB%B9%84%EB%B0%94%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%A6%88%EC%BD%94%EB%A6%AC%EC%95%84?"
}
seoul_small_company_benefits_url_map = {
    "(주)씨드앤" : "https://www.jobplanet.co.kr/companies/383513/reviews/%EC%94%A8%EB%93%9C%EC%95%A4?",
    "(주)시큐어로그" : "https://www.jobplanet.co.kr/companies/395289/reviews/%EC%8B%9C%ED%81%90%EC%96%B4%EB%A1%9C%EA%B7%B8?",
    "(주)딜라이트룸" : "https://www.jobplanet.co.kr/companies/363631/reviews/%EB%94%9C%EB%9D%BC%EC%9D%B4%ED%8A%B8%EB%A3%B8?",
    "(주)팀엘리시움" : "https://www.jobplanet.co.kr/companies/329950/reviews/%ED%8C%80%EC%97%98%EB%A6%AC%EC%8B%9C%EC%9B%80?",
    "(주)헬로우엠" : "https://www.jobplanet.co.kr/companies/356540/reviews/%ED%97%A8%EB%A1%9C%EC%9A%B0%EC%97%A0?",
    "(주)헥톤프로젝트" : "https://www.jobplanet.co.kr/companies/338878/reviews/%ED%97%A5%ED%86%A4%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8?",
    "(주)골라라" : "https://www.jobplanet.co.kr/companies/385866/reviews/%EA%B3%A8%EB%9D%BC%EB%9D%BC?",
    "(주)건강한친구들" : "https://www.jobplanet.co.kr/companies/389193/reviews/%EA%B1%B4%EA%B0%95%ED%95%9C%EC%B9%9C%EA%B5%AC%EB%93%A4?",
    "(주)식스샵" : "https://www.jobplanet.co.kr/companies/325060/reviews/%EC%8B%9D%EC%8A%A4%EC%83%B5?",
    "(주)코드브릭" : "https://www.jobplanet.co.kr/companies/326791/reviews/%EC%BD%94%EB%93%9C%EB%B8%8C%EB%A6%AD?"
}
daegu_small_company_benefits_url_map = {
    "(주)코그" : "https://www.jobplanet.co.kr/companies/89929/reviews/%EC%BD%94%EA%B7%B8?",
    "제이코프" : "https://www.jobplanet.co.kr/companies/11426/reviews/%EC%A0%9C%EC%9D%B4%EC%BD%94%ED%94%84?",
    "(주)퓨전소프트" : "https://www.jobplanet.co.kr/companies/49821/reviews/%ED%93%A8%EC%A0%84%EC%86%8C%ED%94%84%ED%8A%B8?",
    "라온엔터테인먼트(주)" : "https://www.jobplanet.co.kr/companies/79242/reviews/%EB%9D%BC%EC%98%A8%EC%97%94%ED%84%B0%ED%85%8C%EC%9D%B8%EB%A8%BC%ED%8A%B8?",
    "(주)빅밸류" : "https://www.jobplanet.co.kr/companies/324034/reviews/%EB%B9%85%EB%B0%B8%EB%A5%98?",
    "(주)11마리의낭만고양이" : "https://www.jobplanet.co.kr/companies/330160/reviews/11%EB%A7%88%EB%A6%AC%EC%9D%98%EB%82%AD%EB%A7%8C%EA%B3%A0%EC%96%91%EC%9D%B4?",
    "(주)옥션원" : "https://www.jobplanet.co.kr/companies/385418/reviews/%EC%98%A5%EC%85%98%EC%9B%90?",
    "(주)데이타뱅크" : "https://www.jobplanet.co.kr/companies/81254/reviews/%EB%8D%B0%EC%9D%B4%ED%83%80%EB%B1%85%ED%81%AC?",
    "포위즈시스템(주)" : "https://www.jobplanet.co.kr/companies/50066/reviews/%ED%8F%AC%EC%9C%84%EC%A6%88%EC%8B%9C%EC%8A%A4%ED%85%8C%EC%85%98?",
    "(주)위니텍" : "https://www.jobplanet.co.kr/companies/60695/reviews/%EC%9C%84%EB%8B%88%ED%85%8D?"
}

ALL_URLS = {**seoul_big_company_benefits_url_map,
            **seoul_frorein_company_benefits_url_map,
            **seoul_small_company_benefits_url_map,
            **daegu_small_company_benefits_url_map}

TARGET_TITLES = ["의료/건강","지원 제도","교통/출퇴근","급여/보상","연차/휴가","근무환경","교육/자기계발"]

# ---------- Selenium 설정 ----------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def make_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,2000")
    # 필요시 사용자 에이전트 지정
    opts.add_argument("user-agent=Mozilla/5.0")
    return webdriver.Chrome(options=opts)

def to_benefits_url(url: str) -> str:
    # /benefits/ 
    if "/reviews/" in url:
        return url.replace("/reviews/", "/benefits/")
    # 이미 benefits면 그대로
    if "/benefits/" in url:
        return url
    # 마지막에 benefits 추가
    if url.endswith("?"):
        return url[:-1] + "/benefits?"
    return url.rstrip("/") + "/benefits"

def fetch_welfare_by_category_selenium(driver, url: str, timeout=12) -> dict:
    """
    정확 위치:
      #welfare-item-list > div > div > ul > li > div
        └ h5.welfare-bullet__tit (카테고리)
        └ ul.welfare-bullet__list > li (키워드)
    """
    target = to_benefits_url(url)
    driver.get(target)

    # 복지 리스트 컨테이너
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#welfare-item-list div.welfare-bullet"))
        )
    except Exception:
        # 로딩지연 방지
        time.sleep(2)

    result = {}
    blocks = driver.find_elements(By.CSS_SELECTOR,
        "#welfare-item-list > div > div > ul > li > div")
    for div in blocks:
        try:
            title_el = div.find_element(By.CSS_SELECTOR, "h5.welfare-bullet__tit")
            title = title_el.text.strip()
            if title not in TARGET_TITLES:
                continue
            items_els = div.find_elements(By.CSS_SELECTOR, "ul.welfare-bullet__list > li")
            items = []
            for it in items_els:
                t = it.text.strip()
                if t:
                    items.append(t)
            if items:
                result.setdefault(title, []).extend(items)
        except Exception:
            continue
    return result

def crawl_all_benefits() -> dict:
    driver = make_driver(headless=True)
    all_cat_items = defaultdict(list)
    try:
        for name, url in ALL_URLS.items():
            print(f"[크롤링] {name} …")
            try:
                data = fetch_welfare_by_category_selenium(driver, url)
                if not data:
                    print("  └─ (메모) 복지 항목을 찾지 못했거나 로그인 필요 페이지일 수 있음")
                for cat, items in data.items():
                    all_cat_items[cat].extend(items)
            except Exception as e:
                print(f"  └─ 오류: {e}")
    finally:
        driver.quit()
    return all_cat_items

def make_wordcloud(freq: Counter, title: str, outpath: str):
    if not freq:
        print(f"[SKIP] {title} 데이터 없음"); 
        return
    wc = WordCloud(font_path=FONT_PATH, width=900, height=900,
                   background_color="white", colormap="Set3", max_font_size=260)
    cloud = wc.generate_from_frequencies(freq)
    cloud.to_file(outpath)
    print(f"[SAVE] {outpath}")
    plt.figure(figsize=(9,9)); plt.axis("off"); plt.imshow(cloud); plt.title(title); plt.show()

def save_freq_csv(freq: Counter, path_csv: str, cols=("키워드","빈도")):
    if not freq: return
    df_ = pd.DataFrame(sorted(freq.items(), key=lambda x:(-x[1], x[0])), columns=list(cols))
    df_.to_csv(path_csv, index=False, encoding="utf-8-sig")
    print(f"[SAVE] {path_csv}")

# ===== 실행 (복지 → 워드클라우드) =====
cat_items = crawl_all_benefits()

overall_counter = Counter()
for cat, items in cat_items.items():
    c = Counter(items)
    overall_counter.update(c)
    make_wordcloud(c, f"{cat} 워드클라우드", f"./benefit_outputs/{cat}_wordcloud.jpg")
    save_freq_csv(c, f"./benefit_outputs/{cat}_freq.csv")

make_wordcloud(overall_counter, "전체 복지 워드클라우드", "./benefit_outputs/_overall_wordcloud.jpg")
save_freq_csv(overall_counter, "./benefit_outputs/_overall_keyword_freq.csv")

# 카테고리별 합계 빈도 CSV
cat_sum = {cat: sum(Counter(items).values()) for cat, items in cat_items.items()}
pd.DataFrame(sorted(cat_sum.items(), key=lambda x:(-x[1], x[0])),
             columns=["카테고리","합계빈도"]).to_csv(
                 "./benefit_outputs/_category_total_freq.csv",
                 index=False, encoding="utf-8-sig"
             )
print("[A DONE] 복지 워드클라우드 산출 완료")

# =========================================================
# B) 그룹별 평균연봉(막대) + 평점(꺾은선)
#    - CSV: ./jobplanet_company_300.csv
#    - 회사명 매칭으로 그룹별 평균 집계
# =========================================================

CSV_PATH = "./jobplanet_company_300.csv"
for enc in ["utf-8", "utf-8-sig", "cp949"]:
    try:
        df = pd.read_csv(CSV_PATH, encoding=enc)
        print(f"[LOAD] {CSV_PATH} (encoding={enc})")
        break
    except Exception:
        if enc == "cp949":
            raise

# 그룹 정의 (회사명 리스트)
GROUP_MAP = {
    "서울 대기업": list(seoul_big_company_benefits_url_map.keys()),
    "서울 외국계기업": list(seoul_frorein_company_benefits_url_map.keys()),
    "서울 중소기업": list(seoul_small_company_benefits_url_map.keys()),
    "대구 중소기업": list(daegu_small_company_benefits_url_map.keys()),
}

def _to_numeric_series(s: pd.Series):
    if s is None:
        return pd.Series(dtype="float64")
    s = s.astype(str).str.replace(r"[^\d\.]", "", regex=True)
    return pd.to_numeric(s, errors="coerce")

salary_col_candidates = ["평균연봉","연봉(만원)","연봉(원)","연봉","평균연봉(만원)"]
rating_col_candidates = ["평점","기업평점","총평점"]
salary_col = next((c for c in salary_col_candidates if c in df.columns), None)
rating_col = next((c for c in rating_col_candidates if c in df.columns), None)

if salary_col is None or rating_col is None:
    print("[경고] 연봉/평점 컬럼을 찾지 못했습니다. CSV 컬럼명을 확인하세요.")
else:
    # 회사명 컬럼 보정
    if "회사명" not in df.columns:
        print("[경고] '회사명' 컬럼이 없습니다. 회사명 매칭이 필요합니다.")
        df["회사명"] = ""

    df["_salary_num"] = _to_numeric_series(df[salary_col])
    df["_rating_num"] = _to_numeric_series(df[rating_col])

    rows = []
    for gname, companies in GROUP_MAP.items():
        sub = df[df["회사명"].isin(companies)]
        avg_salary = sub["_salary_num"].mean(skipna=True)
        avg_rating = sub["_rating_num"].mean(skipna=True)
        cnt = len(sub)
        rows.append((gname, avg_salary, avg_rating, cnt))
    group_stats = pd.DataFrame(rows, columns=["그룹","평균연봉","평점","기업수"]).set_index("그룹").sort_index()

    # 연봉 단위(만원)로 보정
    salary_scale = 1.0
    salary_unit = "만원"
    if group_stats["평균연봉"].max() > 1_000_000:
        salary_scale = 10_000.0   # 원 → 만원
        salary_unit = "만원"

    x = np.arange(len(group_stats.index))
    sal = (group_stats["평균연봉"] / salary_scale).values
    rat = group_stats["평점"].values

    fig, ax1 = plt.subplots(figsize=(12, 6))
    bars = ax1.bar(group_stats.index, sal, alpha=0.85, label=f"평균연봉({salary_unit})")
    ax1.set_ylabel(f"평균연봉({salary_unit})", fontsize=12)
    ax1.set_xlabel("그룹", fontsize=12)

    for b, v in zip(bars, sal):
        if np.isnan(v): continue
        ax1.text(b.get_x()+b.get_width()/2, v + (max(sal[np.isfinite(sal)])*0.02 if np.isfinite(sal).any() else 0.2),
                 f"{v:,.0f}", ha="center", va="bottom", fontsize=10)

    ax2 = ax1.twinx()
    ax2.plot(group_stats.index, rat, marker="o", linewidth=2, label="평점")
    ax2.set_ylabel("평점", fontsize=12)
    # 평점 5점 만점 가정
    ymax_r = np.nanmax(rat) if np.isfinite(rat).any() else 5
    ax2.set_ylim(0, max(5, ymax_r + 0.5))

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, loc="upper left")

    plt.title("그룹별 평균연봉(막대) & 평점(꺾은선)", fontsize=14, fontweight="bold")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

    group_stats_out = "./benefit_outputs/_group_salary_rating_summary.csv"
    group_stats.to_csv(group_stats_out, encoding="utf-8-sig")
    print(f"[SAVE] {group_stats_out}")

print("[B DONE] 그룹별 평균연봉/평점 그래프 산출 완료")
print("[ALL DONE]")
