import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

def main():
    # url = "https://series.naver.com/novel/detail.series?productNo=2406723"
    # html = urlopen(url)
    # bsObject = BeautifulSoup(html, "html.parser")
    # print(bsObject)

    # Chrome WebDriver 경로
    webdriver_path = 'C:/Users/lenovo/Downloads/chromedriver_win32/chromedriver'

    # Chrome WebDriver 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 브라우저를 화면에 표시하지 않음
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    # WebDriver 서비스 시작
    service = Service(webdriver_path)
    service.start()

    # WebDriver 생성
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 웹 페이지 로드
    url = 'https://series.naver.com/novel/detail.series?productNo=1200383'
    driver.get(url)

    # display: none;으로 숨겨진 요소를 포함하는 div의 클래스명
    div_class = '_synopsis'

    # 숨겨진 요소를 포함하는 div 요소를 찾기 위한 XPath
    xpath = f"//div[contains(@class, '{div_class}') and contains(@style, 'display: block;')]"

    # 숨겨진 요소를 포함하는 div 요소 가져오기
    hidden_div = driver.find_element(By.XPATH, xpath)

    # 데이터 추출
    description = hidden_div.text
    print(description)

    # WebDriver 종료
    driver.quit()

if __name__ == '__main__':
    main()

# selenium 사용해야 할듯
# 그리고 태그는 잘나옴