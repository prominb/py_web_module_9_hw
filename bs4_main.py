import json

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com"


def get_quotes():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('span', class_='text')
    # print(quotes)  # print(type(quotes))
    for quote in quotes:
        print(quote)


def get_authors():
    pass


def main():
    get_quotes()


if __name__ == '__main__':
    main()
