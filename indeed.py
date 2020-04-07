import requests, csv
import os
from bs4 import BeautifulSoup

class Crawling():
    isFirst = True

    def __init__(self):
        # URL을 입력받아 변수에 저장한다.
        self.url = "https://kr.indeed.com/jobs?q=python&limit=50"

    #HTML을 파싱해 텍스트 형태로 변수에 저장 해놓음
    def getHTML(self, cnt):
        if self.isFirst == True:
            print("Getting html...")
        
        res = requests.get(self.url + "&start=" + str(cnt * 50))
        # &start=50, 100 등이 의미하는 것은 각 페이지를 방문하는 주소이다.

        # HTTP response의 성공값이 200이 아닐경우에 에러 메세지를 출력하며
        # 프로그램을 종료한다
        if res.status_code != 200:
            print('\n'+'=' * 35)
            print("Page can't be loaded : " + str(res.status_code) + " Error")
            print('=' * 35)
            os._exit(1)
        # https://kr.indeed.com/dooyeong 와 같은 없는 페이지 url을
        # 크롤링 하려고 시도하면 404 에러가 발생하며 프로그램이 종료됨
        else:
            if self.isFirst == True:
                print("Getting html: Success!\n")
                self.isFirst = False

        # 요청값에서 텍스트를 가져온 후 BS을 이용해 html을 파싱한다
        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        return soup

    def getPages(self,soup):

        # div pagination 클래스 태그 하위의 앵커 태그들을 선택한다 (a태그들의 개수)
        pages = soup.select(".pagination > a")

        return len(pages)

    def writeCSV(self, jobID, jobTitle, jobLocation, cnt):

        # encoding의 한글 호환 문제 때문에 UTF8 형태로 인코딩 해주는 encoding를 추가해주었다
        file = open("indeed.csv", "a", newline="", encoding='UTF8')
        wr = csv.writer(file)

        # 크롤링한 카드의 개수만큼 i로 순회해주며 파일에 쓴다
        for i in range(len(jobID)):
            wr.writerow([str(i + 1 + (cnt * 50)), jobID[i], jobTitle[i], jobLocation[i]]) 

        file.close

    def getCards(self,soup,cnt):
        
        # 각 카드들을 div 태그 하위 클래스를 특정해주어 모두 변수에 저장해준다 
        jobCards = soup.find_all("div", class_="jobsearch-SerpJobCard")

        # 크롤링할 정보들을 List 형태로 받기 위해 빈 List를 선언해준다
        jobID = []
        jobTitle = []
        jobLocation = []

        # 각각의 카드를 card 변수로 순회하며 크롤링을 수행한다
        for card in jobCards:
            jobID.append("https://kr.indeed.com/viewjob?jk=" + card["data-jk"])
            
            # 가독성을 위해 개행문자를 삭제해준다 (replace)
            jobTitle.append(card.find("a").text.replace("\n",""))

            # 첫 번째 카드와 이외의 카드들의 태그가 다르게 되어 있으므로 조건식으로
            # 구별해 List에 삽입해준다
            if card.find("div",class_="location") != None:
                jobLocation.append(card.find("div",class_="location").text)
            elif card.find("span",class_="location") != None:
                jobLocation.append(card.find("span",class_="location").text)

        self.writeCSV(jobID,jobTitle,jobLocation,cnt)


    # Crawling 함수의 메인 함수격이다. 모든 일을 수행한다
    def crawl(self):

        soupPage = self.getHTML(0)
        print('=' * 30)
        print("Start Getting Cards' informations\n")
        pages = self.getPages(soupPage)

        # 파일을 열어 최초 한번 초기화된 상태로 첫 번째 행의 정보를 쓴다
        file = open("indeed.csv", "w", newline="", encoding='UTF8')
        wr = csv.writer(file)
        wr.writerow(["No.","Link","Title","Location"])
        file.close

        # 각 페이지별로 soup을 긁어와 i변수로 순회하며 크롤링해서 csv파일에 쓴다
        for i in range (pages):
            soupCard = self.getHTML(i)
            self.getCards(soupCard,i)
            print("Writing in csv..." + str(int((i+1) * 100 /pages)) + "% Done")


# 메인 함수이다 
if __name__ == "__main__":

    s = Crawling()
    s.crawl()
    print('\n===== HTML Crawling Complete ! =====')