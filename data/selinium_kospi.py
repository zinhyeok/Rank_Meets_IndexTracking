from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta
import chromedriver_autoinstaller 

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
# KRX 데이터 페이지 접속
driver.get('http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201010106')

# 검색버튼 클릭
search_button = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#btnindIdx_finder_equidx0_0'))
)
# 종목 입력
search_button.click()

# 코스피 항목 클릭
kospi_field = WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#FORM__finder_equidx0_0 > div.pb15.pt15.pl20.pr20 > label:nth-child(6)'))
)
# 종목 입력
kospi_field.click()

# 코스피 클릭
kospi = WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#jsGrid__finder_equidx0_0 > tbody > tr:nth-child(1) > td.tal.pl20'))
)
# 종목 입력
kospi.click()

# 시작 날짜와 끝 날짜 설정
start_date = datetime.strptime('20060101', '%Y%m%d')
end_date = datetime.strptime('20221231', '%Y%m%d')

current_date = start_date

while current_date <= end_date:
    date_str = current_date.strftime('%Y%m%d')
    try:        
        # 날짜 입력 필드 찾기
        date_field = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#trdDd'))
        )
        
        # 날짜 입력
        date_field.clear()
        date_field.send_keys(date_str)
        
        # 조회 버튼 클릭
        search_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#jsSearchButton'))
        )
        search_button.click()
        
        # 데이터 유무 확인
        time.sleep(10)  # 조회 후 페이지가 로드될 시간을 줌

        no_data_message = "데이터가 없습니다."
        if no_data_message in driver.page_source:
            print(f"No data for date: {date_str}")
            current_date += timedelta(days=1)
            continue
        
        # 다운로드 이미지 버튼 클릭
        download_img_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#UNIT-WRAP0 > div.time.CI-MDI-UNIT > p:nth-child(2) > button.CI-MDI-UNIT-DOWNLOAD > img'))
        )
        download_img_button.click()
        
        # 다운로드 엑셀 버튼 클릭
        download_xls_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#ui-id-3 > div > div:nth-child(1) > a'))
        )
        download_xls_button.click()
        
        # 다운로드 대기 시간
        time.sleep(5)  # 다운로드 시간에 따라 조절 필요

    except Exception as e:
        print(f"Error on date {date_str}: {e}")

    # 다음 날짜로 이동
    current_date += timedelta(days=1)

# 드라이버 종료
driver.quit()
