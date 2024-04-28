import json

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com"


def get_quotes():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    # quotes = soup.find_all('span', class_='text')
    # print(quotes)  # print(type(quotes))
    # for quote in quotes:
    #     print(quote.text)
    quotes_list = [quote.text for quote in soup.find_all('span', class_="text")]
    # for quote in quotes_list:
    #     print(quote)
    authors_list = [author.text for author in soup.find_all('small', class_="author")]
    # for author in authors_list:
    #     print(author)
    tags_list = [tag.text.replace('Tags:', '').strip().split('\n') for tag in soup.find_all('div', class_="tags")]
    for tags in tags_list:
        print(tags)


def get_authors():
    pass


def main():
    get_quotes()


if __name__ == '__main__':
    main()
