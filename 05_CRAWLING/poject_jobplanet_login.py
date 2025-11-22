"""
잡플래닛 회사 평점 크롤링
- 전체 평점
- 복지 및 급여
- 업무와 삶의 균형 등

회사명: class=name

https://www.jobplanet.co.kr/companies/30139/reviews/%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90

https://wikidocs.net/149338 

"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys  import Keys
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate

company_dict = {'삼성전자':'https://www.jobplanet.co.kr/companies/30139/reviews/삼성전자',
                'LG전자':'https://www.jobplanet.co.kr/companies/19514/reviews/lg전자',
                'SK하이닉스':'https://www.jobplanet.co.kr/companies/20561/reviews/에스케이하이닉스',
                '네이버':'https://www.jobplanet.co.kr/companies/42217/reviews/네이버'}

# xpath_dict_old = {'전체평점': '//*[@id="premiumReviewStatistics"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/span[1]',                      
#               '복지': '//*[@id="premiumReviewStatistics"]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/span[2]',
#               '워라벨': '//*[@id="premiumReviewStatistics"]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/span[2]',
#               '사내문화': '//*[@id="premiumReviewStatistics"]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/div[3]/div[2]/span[2]',
#               '승진 기회': '//*[@id="premiumReviewStatistics"]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/span[2]',
#               '경영진': '//*[@id="premiumReviewStatistics"]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/div[5]/div[2]/span[2]'}

user_id = '@gmail.com'
passwd = '!'

def  login(driver,  user_id,  pwd):
    driver.get("https://www.jobplanet.co.kr/users/sign_in?_nav=gb")
    time.sleep(1)

    # 아이디 입력
    login_id  =  driver.find_element(By.ID,  "user_email")
    login_id.send_keys(user_id)

    # 비밀번호 입력
    login_pwd  =  driver.find_element(By.ID,  "user_password")
    login_pwd.send_keys(pwd)

    # 로그인 버튼 클릭
    login_id.send_keys(Keys.RETURN)
    time.sleep(5)


# --- get_review_score: 저장 대신 DataFrame 반환 ---
def get_review_score(driver):    
    compary_score_dict = {}  # {'삼성전자': [전체, 복지/급여, 워라밸, 사내문화, 승진기회, 경영진]}
    score_columns = None     # 컬럼명(한 번만 세팅)

    for company_name in company_dict.keys():
        score_title_list = []  # 평점 이름(전체 평점, 복지/급여, ...)
        score_list = []
        
        company_url = company_dict.get(company_name)
        driver.get(company_url)
        time.sleep(2)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 전체 평점
        total_score = soup.select_one('span.rate_point').text
        score_title_list.append('전체 평점')
        score_list.append(float(total_score))

        # 세부 평점
        rate_bar_group = soup.select_one('div.rate_bar_group')
        point_title_list = rate_bar_group.select('div.rate_bar_title')
        for title in point_title_list:
            score_title_list.append(title.text.strip())

        txt_point_list = rate_bar_group.select('span.txt_point')
        for point in txt_point_list:            
            score_list.append(float(point.text))  # 실수 변환

        # 첫 회사에서만 컬럼명 고정
        if score_columns is None:
            score_columns = score_title_list[:]

        # 딕셔너리에 저장
        compary_score_dict[company_name] = score_list

    # DataFrame으로 반환(저장은 main에서)
    df_scores = pd.DataFrame.from_dict(compary_score_dict, orient='index', columns=score_columns)
    df_scores.index.name = '기업명'
    return df_scores


# --- get_company_info: 저장 대신 DataFrame 반환 ---
def get_company_info(driver):
    company_info_dict = {}  # {'삼성전자': [산업, 기업형태, 사원수, 설립일]}
    info_columns = None

    for company_name in company_dict.keys():
        company_url = company_dict.get(company_name)
        driver.get(company_url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # ▼ (당신 코드 틀 유지: 선택자만 최소 보정 필요 시 해주세요)
        #   'span.block text-body2 text-gray-300' → 'span.block.text-body2.text-gray-300'
        #   'section.w-[1060px] mx-auto pb-[120px]' → 'section.w-\\[1060px\\].mx-auto.pb-\\[120px\\]'
        info_bar_group = soup.select_one('section.w-\\[1060px\\].mx-auto.pb-\\[120px\\]') or soup

        # 라벨(제목)
        title_elems = info_bar_group.select('span.block.text-body2.text-gray-300')
        info_title_list = [t.get_text(strip=True) for t in title_elems if t.get_text(strip=True)]

        # 값(내용)
        value_elems = info_bar_group.select('strong.mt-\\[6px\\].block.text-h8.text-gray-800, strong.text-h8')
        infoname_list = [v.get_text(strip=True) for v in value_elems if v.get_text(strip=True)]

        # 개수 맞추기(최소 길이)
        n = min(len(info_title_list), len(infoname_list))
        info_title_list = info_title_list[:n]
        infoname_list = infoname_list[:n]

        # 첫 회사에서만 컬럼명 고정 (예: ['산업','기업형태','사원수','설립일'])
        if info_columns is None:
            info_columns = info_title_list[:]

        company_info_dict[company_name] = infoname_list

    df_info = pd.DataFrame.from_dict(company_info_dict, orient='index', columns=info_columns)
    df_info.index.name = '기업명'
    return df_info


# --- main: 두 DF를 회사명(인덱스) 기준으로 합치고 한 번에 저장 ---
def main():
    driver = webdriver.Chrome()

    # login(driver, user_id, passwd)  # 필요 시 활성화
    df_scores = get_review_score(driver)   # 평점류
    df_info   = get_company_info(driver)   # 기업정보류

    # 회사명(인덱스) 기준 병합
    df_all = df_scores.join(df_info, how='outer')  # 공통키(기업명) 기준

    # 저장 (한 파일로)
    df_all.to_csv("company_all.csv", encoding="utf-8-sig", index=True)
    df_all.to_excel("company_all.xlsx", index=True)
    print("Saved: company_all.csv / company_all.xlsx")

    time.sleep(2)
    driver.close()

main()
