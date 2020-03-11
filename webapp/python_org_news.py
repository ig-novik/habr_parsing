from datetime import datetime

import requests
from bs4 import BeautifulSoup

from webapp.model import db, News

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False

def get_python_news():
    html = get_html("http://www.python.org/blogs/")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='list-recent-posts').findAll('li')
        result_news = []
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time').text
            try:
                published = datetime.strptime(published, '%Y-%m-%d')
            except:
                published = datetime.now()
            result_news.append({
                "title": title,
                "url": url,
                "published": published
            })
        return  result_news
    return False

def save_news(title, urk, published):
    news_news = News(title=title, url=url, published=published)