import os
import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response.text


def parse_and_save_articles(base_url, start_page, end_page, output_folder):
    for page_num in range(start_page, end_page + 1):
        url = f"{base_url}/doc/{page_num}"
        html = get_html(url)

        soup = BeautifulSoup(html, 'html.parser')

        article_text = soup.find('div', class_='Article--text')

        # Проверка наличия блока с классом "Article--text"
        if article_text:
            paragraphs = article_text.find_all(['p', 'ul', 'li'])

            output_file_path = os.path.join(output_folder, f'kaktus{page_num}.txt')
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                for element in paragraphs:
                    if element.name == 'ul':
                        for li in element.find_all('li'):
                            output_file.write(f'- {li.text}\n')
                    elif element.name == 'li':
                        output_file.write(f'- {element.text}\n')
                    else:
                        output_file.write(element.text + '\n')

                print(f"Статья {page_num} сохранена в {output_file_path}")
        else:
            print(f"Статья {page_num} не содержит блока 'Article--text'")


base_url = 'https://kaktus.kg'
start_page = 2
end_page = 15049
output_folder = 'outputs/articles/kaktus'

parse_and_save_articles(base_url, start_page, end_page, output_folder)
