import json

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com"


def get_quotes():
    json_list = list()
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
    # for tags in tags_list:
    #     print(tags)
    # json_list = li
    for quote, author, tags in zip(quotes_list, authors_list, tags_list):
        # print(author, quote, tags)
        json_list.append(
            {
                "tags": tags,
                "author": author,
                "quote": quote
            }
        )
    # print(json_list)
    print(write_to_json("quotes.json", json_list))


def get_authors():
    pass


def write_to_json(filename, json_list):
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(json_list, fh, indent=4)
    return "DONE."


def main():
    get_quotes()


if __name__ == '__main__':
    main()
