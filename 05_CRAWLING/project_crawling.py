from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, pandas as pd

BASE = "https://www.jobplanet.co.kr"
END_PAGE = 622

def safe_text(el, xp):
    try:
        return el.find_element(By.XPATH, xp).text.strip()
    except:
        return None

def parse_review_count(txt: str):
    """'2,823개의 리뷰' 같은 문자열에서 숫자만 뽑아 int로 반환"""
    if not txt:
        return None
    digits = "".join(ch for ch in txt if ch.isdigit())
    return int(digits) if digits else None

def crawl_list_pages(driver, industry_id=700, end_page=END_PAGE):
    rows = []
    wait = WebDriverWait(driver, 15)
    for page in range(1, end_page+1):
        url = f"{BASE}/companies?industry_id={industry_id}&page={page}"
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.ID, "listCompanies")))

        # 각 회사 카드(section.company)
        cards = driver.find_elements(By.CSS_SELECTOR, "#listCompanies section.company")
        if not cards:
            cards = driver.find_elements(By.CSS_SELECTOR, "#listCompanies section")

        for order, sec in enumerate(cards, start=1):
            # 회사명 / 링크 (dl[1]/dt/a)
            try:
                name_el = sec.find_element(By.XPATH, ".//dl[1]/dt/a")
                name = name_el.text.strip()
                href = name_el.get_attribute("href") or name_el.get_attribute("data-href") or ""
                if href and not href.startswith("http"):
                    href = BASE + href
            except:
                continue

            # 업종/지역
            industry = safe_text(sec, ".//dl[1]/dd[1]/span[1]")
            location = safe_text(sec, ".//dl[1]/dd[1]/span[3]")

            # 평점/연봉
            overall  = safe_text(sec, ".//dl[2]/dd[1]//span") or safe_text(sec, ".//dl[2]/dd[1]")
            avg_pay  = safe_text(sec, ".//dl[2]/dd[2]//strong") or safe_text(sec, ".//dl[2]/dd[2]")

            # 리뷰개수 (예: '2,823개의 리뷰' → 2823)
            review_text = safe_text(sec, ".//dl[2]/dt")
            review_count = parse_review_count(review_text)

            rows.append({
                "page": page,
                "order": order,
                "company": name,
                "detail_url": href,
                "industry": industry,
                "location": location,
                "overall_rating": overall,
                "avg_salary": avg_pay,
                "review_count": review_count  # ← 추가
            })

        time.sleep(0.2)  # 매너 딜레이
    return pd.DataFrame(rows)

if __name__ == "__main__":
    opts = Options()
    # opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    driver = webdriver.Chrome(options=opts)

    try:
        df = crawl_list_pages(driver, industry_id=700, end_page=622)
        df.to_excel("jobplanet_list_622.xlsx", index=False, engine="openpyxl")
        df.to_csv("jobplanet_list_622.csv", index=False, encoding="utf-8-sig")
        print(df.head(10))
        print("총 수집:", len(df))
    finally:
        driver.quit()
