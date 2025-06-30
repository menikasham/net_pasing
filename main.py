import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

UA = UserAgent(
    fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
HEADERS = {"User-Agent": UA.random}

INVEST_URL = "https://habr.com/ru/articles/"
MAIN_URL = 'https://habr.com'


def get_html(url):
    """Получаем html-код страницы"""
    r = requests.get(url, headers=HEADERS)
    return r.text


def get_text(new_url):
    """Получаем полный текст статьи"""
    temp_link = MAIN_URL + new_url
    soup2 = BeautifulSoup(get_html(temp_link), 'lxml')
    txt = soup2.find('div',
                     class_='article-formatted-body').get_text()
    return txt


def check_words(word: str):
    """Проверяем текст статьи на наличие ключевых слов"""
    count = 0
    for item in KEYWORDS:
        if item in word:
            count += 1
    if count == 0:
        return False
    else:
        return True


def get_data():
    full_data = []
    soup = BeautifulSoup(get_html(INVEST_URL), 'lxml')
    articles = soup.find('div', class_='tm-articles-list').find_all('article')
    for article in articles:
        data = {}
        data.clear()
        data['time'] = article.find('time')['datetime'].split('T')[0]
        data['headline'] = article.find('h2').find('a').find('span').text
        data['link'] = article.find('a', class_="tm-title__link")['href']
        if check_words(get_text(data['link'])):
            full_data.append(data)
    return full_data


def main():
    lst = get_data()
    for item in lst:
        print(f"{item['time']} - {item['headline']} - {MAIN_URL+item['link']}")


if __name__ == "__main__":
    main()
