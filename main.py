import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

titles = []  # 제목을 담을 배열
authors = []  # 작가 이름을 담을 배열
productNum = [] # 소설의 정확한 설명을 담기 위해 상세 페이지 Num을 담을 배열

for page in range(0, 3168):  # 1부터 3168까지의 페이지를 순환, 1969번 파일 손상
    url = f"https://series.naver.com/novel/categoryProductList.series?categoryTypeCode=all&genreCode=&orderTypeCode=sale&is&isFinished=false&page={page}"
    html = urlopen(url)
    bsObject = BeautifulSoup(html, "html.parser")

    title_tags = bsObject.find_all("a", attrs={"title": True, "class": lambda value: value and "NPI=a:content" in value})

    page_titles = [tag["title"] for tag in title_tags]
    page_num = [tag["href"].split("=")[1] for tag in title_tags]

    titles.extend(page_titles)  # 페이지의 제목을 배열에 추가
    productNum.extend(page_num) # 페이지의 제품번호를 배열에 추가

    author_tags = bsObject.find_all("span", class_="author")

    page_authors = [tag.text for tag in author_tags]

    authors.extend(page_authors)

data = zip(titles, authors, productNum)

# CSV 파일로 저장할 경로와 파일명
csv_file = "저장할 경로"

# CSV 파일에 데이터 저장
with open(csv_file, "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Author", "ProductNum"])  # 헤더 쓰기
    writer.writerows(data)  # 데이터 행으로 저장

print(f"{csv_file} 파일로 저장되었습니다.")