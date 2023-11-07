import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

images = [] # 이미지 url을 담을 배열
descriptions = []  # 소설 설명을 담을 배열
genres = [] # 소설 태그들을 문자열로 만든 후 담을 배열

def load_csv(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            data.append(row)
    return data

def extract_column(data, column_index):
    column_data = []
    for row in data:
        column_data.append(row[column_index])
    return column_data
def main():
    filename = '불러올 파일 경로'  # 불러올 CSV 파일의 경로와 이름으로 변경해주세요
    data = load_csv(filename)
    column_datas = extract_column(data, 2)
    cnt = 0

    # ChromeDriver 옵션 설정
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # 브라우저 창을 띄우지 않고 실행

    service = Service(executable_path='C:/Users/lenovo/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    # 네이버 로그인
    driver.get('https://nid.naver.com/nidlogin.login')
    driver.find_element(By.NAME, 'id').send_keys('')  # 네이버 아이디 입력
    driver.find_element(By.NAME, 'pw').send_keys('')  # 네이버 비밀번호 입력
    driver.find_element(By.CSS_SELECTOR, '.btn_login').click()

    time.sleep(100)  # 로그인이 완료될 때까지 잠시 대기

    for column_data in column_datas:
        cnt += 1

        url = f"https://series.naver.com/novel/detail.series?productNo={column_data}"

        # 크롤링할 페이지 접속
        driver.get(url)
        page_source = driver.page_source

        bsObject = BeautifulSoup(page_source, "html.parser")

        # 이미지 가져오기
        img_tags = bsObject.find_all("meta", property="og:image")

        # 소설 설명 가져오기
        elements = bsObject.select("div._synopsis")
        if len(elements) < 1:
            page_img = ""
            page_dsc = ""
            page_genre = ""

            print(page_img)
            print(page_dsc)
            print(page_genre)

            images.append(page_img)
            descriptions.append(page_dsc)
            genres.append(page_genre)

            continue

        elif len(elements) < 2:
            element = elements[0]

        else:
            element = elements[1]

        # 태그 가져오기
        genre_tags = bsObject.find_all("a", href=lambda value: value and "/novel/categoryProductList.series?categoryTypeCode=genre" in value)

        page_img = [tag["content"] for tag in img_tags]
        page_dsc = element.get_text(strip=True).replace("접기", "")
        page_genre = genre_tags[3].text

        print(page_img)
        print(page_dsc)
        print(page_genre)

        images.extend(page_img)
        descriptions.append(page_dsc)
        genres.append(page_genre)

        print(cnt)

    driver.quit()

    data = zip(images, descriptions, genres)
    csv_file = "C:/Users/lenovo/Desktop/NovelsHobby_데이터수집/네이버시리즈_소설설명4-3.csv"

    with open(csv_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Image", "Description", "Genres"])
        writer.writerows(data)
    print(f"{csv_file} 파일로 저장되었습니다.")

if __name__ == '__main__':
    main()
