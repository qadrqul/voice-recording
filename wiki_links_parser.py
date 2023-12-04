import requests
from bs4 import BeautifulSoup


def get_wikipedia_article_links(language_code, max_articles=5000):
    base_url = f'https://{language_code}.wikipedia.org/wiki/Special:Random'
    article_links = []

    for _ in range(max_articles):
        response = requests.get(base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h1', {'class': 'firstHeading'}).text
            url = response.url

            if not any(char.isdigit() for char in title):
                article_links.append(url)
        else:
            print(f"Error fetching article. Status code: {response.status_code}")

    return article_links


def save_links_to_file(links, file_path='outputs/wikipedia_links.txt'):
    with open(file_path, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(f"{link}\n")


if __name__ == "__main__":
    language_code = 'ky'
    max_articles = 2000

    wikipedia_links = get_wikipedia_article_links(language_code, max_articles)
    save_links_to_file(wikipedia_links)
    print(f"{max_articles} Links have been saved to 'outputs/wikipedia_links.txt'.")
