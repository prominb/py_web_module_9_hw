import json

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com"
FILE_QUOTES = "quotes.json"

json_list = list()
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, 'lxml')


def get_quotes() -> list[dict]:
    quotes_list = [quote.text for quote in soup.find_all('span', class_="text")]
    authors_list = [author.text for author in soup.find_all('small', class_="author")]
    tags_list = [tag.text.replace('Tags:', '').strip().split('\n') for tag in soup.find_all('div', class_="tags")]
    for quote, author, tags in zip(quotes_list, authors_list, tags_list):
        json_list.append(
            {
                "tags": tags,
                "author": author,
                "quote": quote
            }
        )
    print(write_to_json(FILE_QUOTES, json_list))


def get_authors():
    # get_author_link = soup.find_all('a')
    # print(get_author_link)
    # for lk in get_author_link:
    #     print(lk["href"])
    # get_author_links = get_author_link["href"]
    # print(get_author_links)
    # get_author_links = soup.find_all(string="(about)")
    # print(get_authors_link)
    get_author_links = soup.find_all('a', string="(about)")
    # print(get_author_links)
    for lk in get_author_links:
        # print(type(lk["href"]), lk["href"])
        print(BASE_URL + lk["href"])


def write_to_json(filename, data):
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=4)
    return f"Save {filename}"


def get_next_page():
    # href = soup.select("[href^='/page/']")
    # print(type(href), len(href), href)
    get_href = soup.select("li.next a")
    # print(get_href)
    get_page_link = get_href[0].attrs
    # print(type(get_link["href"]), get_link["href"])
    return get_page_link


def main():
    # get_quotes()
    get_authors()
    # get_next_page()


if __name__ == '__main__':
    main()
