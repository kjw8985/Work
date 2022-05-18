import requests
from bs4 import BeautifulSoup
import time
import datetime
import pymysql

def news_crawling():
    def insert():
        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='03191121asd!@',
                               db='joomo',
                               charset='utf8')

        sql = "INSERT IGNORE INTO board_boardnews (title, href, datecreated) VALUES (%s, %s, %s)"

        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (title, url, datecreated))
                conn.commit()


    dt_now = datetime.datetime.now()
    result = dt_now.strftime('%Y년 %m월 %d일'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
    datecreated = result
    header = {'User-agent' : 'Mozila/2.0'}

    for i in range(1, 10):

        response = requests.get('https://land.naver.com/news/headline.naver?bss_ymd', headers=header)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.select('ul.headline_list li > dl > dt:nth-child(2)')

            for link in links:
                title = link.text
                url = 'http://land.naver.com'+link.a['href']
                datecreated = dt_now.date()
                print(title, url, datecreated)
                insert()

        else:
            print(response.status_code)

        response = requests.get('https://realestate.daum.net/news', headers=header)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.select('.section_allnews > div > ul > li > a')
            for link in links:
                title = link.text.strip()
                url = link.attrs['href']
                print(title, url, datecreated)
                insert()

        else:
            print(response.status_code)

        time.sleep(900)

news_crawling()