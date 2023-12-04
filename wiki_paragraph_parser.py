import requests
from bs4 import BeautifulSoup
import os

if not os.path.exists('outputs/articles/wiki'):
    os.makedirs('outputs/articles/wiki')

with open('outputs/wikipedia_links.txt', 'r', encoding='utf-8') as file:
    links = file.read().splitlines()

for link in links:
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1').text.strip()
        for element in soup(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', {'class': 'reflist'}, 'table']):
            element.decompose()
        content = soup.find('div', {'id': 'mw-content-text'}).text.strip()
        file_path = os.path.join('outputs/articles/wiki', f'{title}.txt')

        with open(file_path, 'w', encoding='utf-8') as article_file:
            article_file.write(content)
        print(f"Статья '{title}' сохранена в файл {file_path}")
    else:
        print(f"Не удалось получить доступ к статье по ссылке: {link}")
