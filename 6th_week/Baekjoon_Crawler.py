# 산업보안학과 20161247 정두영
# Seleninum과 BeaurifulSoup을 이용한 백준(사이트) 크롤러

# 백준이라는 사이트는 프로그래밍 연습(problem solving)을 위한 사이트이며,
# 기업의 코딩테스트 등을 준비할 때 유용하다.
# 백준의 삼성 SW 역량 기출 문제들을 정리해놓은 문제집 내의
# 문제 번호, 문제 이름, 그리고 문제의 정답률을 크롤링 하는 것이 목표이다.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

# 크롬 드라이버의 위치를 잡아준다.
path = os.getcwd() + "/6th_week/chromedriver.exe"
driver = webdriver.Chrome(path)

try:
    print("\n#### Start Crawling ####\n")

    driver.get("https://www.acmicpc.net/") # 크롬 드라이버를 이용해 크롤링을 할 사이트(백준)에 접속한다.
    time.sleep(1)   # 안전하게 시간을 조절해준다.

    keyword = "삼성 SW 역량 테스트 기출" # 검색할 키워드를 설정해준다.
    driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/div/div[2]/ul/li[10]/a/i").click() # 검색창을 활성화 해준다. 
    searchBox = driver.find_element_by_id("header-search") # 검색할 곳을 특정해준다.
    searchBox.send_keys(keyword) # 검색하고자하는 키워드를 설정해 검색을 해준다.
    searchBox.send_keys(Keys.ENTER)
    time.sleep(1)

    driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/div[1]/div[1]/div/ul/li[2]/a").click() # "문제집" 카테고리를 설정해준다.
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="result"]/div[3]/div/h3/a').click() # 첫 번째 검색결과인 "삼성 SW 역량 테스트" 문제집을 선택해준다. 
    time.sleep(1)
    
    problemNumbers = [] # 문제의 번호를 저장할 리스트.
    problemTexts = [] # 문제 이름을 저장할 리스트.
    problemRates = [] # 문제의 정답률을 저장할 리스트.

    html = driver.page_source
    bs = BeautifulSoup(html,"html.parser")
    
    # 해당 문제집의 모든 문제들에 대한 정보를 담는다.
    contents = bs.find("tbody").find_all("td") # 원하는 태크를 설정해준다.

    # 반복문을 돌며 contents내의 여러가지 정보들을 인덱스로 구분하여 각각의 리스트에 저장한다.
    # 이때, 총 6가지의 카테고리들이 연속해서 나타나기 때문에
    # i를 6으로 나눈 나머지를 활용해 인덱싱을 해주었다.
    for i in range(len(contents)):
        if i % 6 == 0: # 6의 배수번째 카테고리: 문제의 번호
            problemNumbers.append(contents[i].text)
        elif i % 6 == 1: # (6의 배수 + 1)번째 카테고리: 문제의 이름
            problemTexts.append(contents[i].text)
        elif i % 6 == 5: # (6의 배수 + 5)번째 카테고리: 문제의 정답률
            problemRates.append(contents[i].text)

    # 문제 하나당 각각 6개의 카테고리를 가지고 있으므로, 총 문제 개수를 파악하기 위해선
    # 전체 contents를 6으로 나눈 값이 필요하다
    for i in range(int(len(contents)/6)):
        print("--------<"+str(i+1)+">--------") # 총 문제중 몇번째 문제인지 표시한다.
        print("No." + problemNumbers[i]) # 해당 문제의 번호를 표시한다.
        print("Title: " + problemTexts[i]) # 해당 문제의 이름을 표시한다.
        print("Correct Rate: " + problemRates[i]) # 해당 문제의 정답률을 표시한다.
        print()
    
# 해당 작업이 끝나고 크롤링이 끝났다고 표시한 후
# 크롤러를 종료한다.
finally:
    print("### Crawling Done ###")
    time.sleep(2)
    driver.quit()