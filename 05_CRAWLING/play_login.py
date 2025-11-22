# -*- coding: utf-8 -*-
# step1. 프로젝트에 필요한 패키지 불러오기
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, math, re
import pandas as pd

# step2. 로그인 정보 및 검색할 회사 미리 정의
USR   = "@naver.com"   # 잡플래닛 ID (이메일)
PWD   = "ap"            # 비밀번호
QUERY = "네이버랩스"               # 검색할 회사명

# --------- 유틸 ----------
def wait_el(driver, by, sel, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, sel)))

def wait_clickable(driver, by, sel, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, sel)))

def safe_text(root, by, sel):
    try:
        return root.find_element(by, sel).text.strip()
    except:
        return None

# step3. 크롬드라이버 실행 및 잡플래닛 로그인 함수
def login(driver, usr, pwd):
    driver.get("https://www.jobplanet.co.kr/users/sign_in?_nav=gb")
    wait_el(driver, By.TAG_NAME, "body")

    # 이메일 / 비밀번호 입력칸 (여러 후보를 시도; 실제 DOM에 맞게 필요 최소로 조정)
    email_sel = "input[type='email'], #user_email, input[name='user[email]']"
    pass_sel  = "input[type='password'], #user_password, input[name='user[password]']"

    email_in = wait_el(driver, By.CSS_SELECTOR, email_sel)
    pass_in  = wait_el(driver, By.CSS_SELECTOR, pass_sel)

    email_in.clear(); email_in.send_keys(usr)
    pass_in.clear();  pass_in.send_keys(pwd)
    pass_in.send_keys(Keys.RETURN)

    # 로그인 완료 신호(검색창 또는 리스트 영역 등장) 대기
    WebDriverWait(driver, 15).until(
        EC.any_of(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#search_bar_search_query")),
            EC.presence_of_element_located((By.ID, "listCompanies"))
        )
    )
    time.sleep(0.5)

# step4. 원하는 회사의 리뷰 페이지까지 이동 함수
def go_to_review_page(driver, query):
    # 상단 검색창 찾기
    search_box = wait_clickable(driver, By.CSS_SELECTOR, "input#search_bar_search_query")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(1.0)

    # 결과 리스트에서 첫 번째 회사명 링크 클릭 (section.company dl[1] dt > a)
    wait_el(driver, By.ID, "listCompanies")
    first_link = wait_clickable(driver, By.CSS_SELECTOR, "#listCompanies section.company dl:nth-of-type(1) dt > a")
    first_link.click()

    # 새 탭이 열릴 수 있으므로 마지막 탭으로 전환
    time.sleep(0.5)
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])

    # 리뷰 탭 이동 (여러 후보 중 가능한 것 클릭)
    try:
        btn = wait_clickable(driver, By.CSS_SELECTOR, "a.viewReviews, a[href*='reviews']")
        btn.click()
    except:
        pass
    time.sleep(1.0)

# step5. 별점 변환 함수 (스타일 width 기반일 때)
def parse_star_rating(style_attribute):
    # 예: "width:60%" → 60 -> 3점
    if not style_attribute:
        return "별점 없음"
    m = re.search(r"(\d+)", style_attribute)
    if not m:
        return "별점 없음"
    pct = int(m.group(1))
    score = round(pct / 20)
    return f"{score}점"

# step6. 데이터 크롤링 함수 (직무/근속여부/일시/요약/평점/장점/단점/경영진에게 바라는 점)
def scrape_data(driver):
    list_div, list_cur, list_date = [], [], []
    list_stars, list_summery = [], []
    list_merit, list_disadvantages, list_opinions = [], [], []

    # 전체 리뷰 개수 파악 (숫자만 추출)
    title = wait_el(driver, By.ID, "viewReviewsTitle")
    num_txt = safe_text(title, By.TAG_NAME, "span") or title.text
    num = int(re.sub(r"[^\d]", "", num_txt)) if re.search(r"\d", num_txt or "") else 0

    # 페이지 수 (페이지당 보통 5개)
    pages = max(1, math.ceil(num / 5))

    for _ in range(pages):
        review_list = wait_el(driver, By.ID, "viewReviewsList")
        review_box = review_list.find_elements(By.TAG_NAME, "section")

        for box in review_box:
            # 상단 유저/직무/재직여부/날짜 영역
            try:
                user_info_area = box.find_elements(By.TAG_NAME, "div")[0]
                user_info = user_info_area.text.split("|")
            except:
                user_info = []

            division = user_info[0].strip() if len(user_info) >= 1 else ""
            current  = user_info[1].strip() if len(user_info) >= 2 else ""
            date     = (user_info[3].strip() if len(user_info) >= 4 else "날짜 없음")

            list_div.append(division)
            list_cur.append(current)
            list_date.append(date)

            # 리뷰 요약
            try:
                summary = box.find_element(By.TAG_NAME, "h2").text.strip()
                list_summery.append(summary)
            except:
                msg = "신고로 인해 리뷰 요약 없음"
                list_summery.append(msg)
                list_merit.append(msg)
                list_disadvantages.append(msg)
                list_opinions.append(msg)

            # 장점/단점/경영진에게 바라는 점
            try:
                review_info_area = box.find_elements(By.TAG_NAME, "dl")[-1]
                contents = review_info_area.find_elements(By.TAG_NAME, "dd")
                list_merit.append(contents[0].text.strip() if len(contents) > 0 else "")
                list_disadvantages.append(contents[1].text.strip() if len(contents) > 1 else "")
                list_opinions.append(contents[2].text.strip() if len(contents) > 2 else "")
            except:
                # 위에서 요약 없음 처리로 이미 채워진 경우가 있어 패스
                pass

            # 별점 (width 스타일 기반)
            try:
                star_spans = box.find_elements(By.TAG_NAME, "span")
                added = False
                for sp in star_spans:
                    style = sp.get_attribute("style") or ""
                    if "width" in style:
                        list_stars.append(parse_star_rating(style))
                        added = True
                        break
                if not added:
                    list_stars.append("별점 없음")
            except:
                list_stars.append("별점 없음")

        # 다음 페이지로
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, ".btn_pgnext")
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", next_btn)
            time.sleep(0.2)
            next_btn.click()
            time.sleep(1.2)
        except:
            break  # 더 이상 없음

    total_data = pd.DataFrame({
        "날짜": list_date,
        "직무": list_div,
        "고용 현황": list_cur,
        "별점": list_stars,
        "요약": list_summery,
        "장점": list_merit,
        "단점": list_disadvantages,
        "경영진에게 바라는 점": list_opinions
    })
    return total_data

# ---------------- main ----------------
def main():
    # 크롬 드라이버 실행
    opts = Options()
    # opts.add_argument("--headless=new")  # 필요 시 헤드리스
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("user-agent=Mozilla/5.0")
    driver = webdriver.Chrome(options=opts)

    try:
        # 로그인
        login(driver, USR, PWD)

        # 리뷰 페이지로 이동
        go_to_review_page(driver, QUERY)

        # 리뷰 크롤링
        total_data = scrape_data(driver)

        # 엑셀 파일로 저장
        out_name = f"잡플래닛 리뷰 총정리_{QUERY}.xlsx"
        total_data.to_excel(out_name, index=True)
        print(f"[DONE] rows={len(total_data)} saved: {out_name}")

    finally:
        # 크롬 드라이버 종료
        driver.quit()

if __name__ == "__main__":
    main()
