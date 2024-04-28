import json
from time import sleep

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com"
FILE_QUOTES = "quotes.json"
FILE_AUTHORS = "authors.json"

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, 'lxml')


def get_quotes() -> list[dict]:
    json_list = list()
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


def get_authors(links_list: list) -> list[dict]:
    if links_list:
        json_list = list()
        for link in links_list:
            sleep(1.2)
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'lxml')
            fullname = soup.find('h3', class_="author-title").text
            born_date = soup.find('span', class_="author-born-date").text
            born_location = soup.find('span', class_="author-born-location").text
            description = soup.find('div', class_="author-description").text.strip()
            json_list.append(
                {
                    "fullname": fullname,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description
                }
            )
        print(write_to_json(FILE_AUTHORS, json_list))
    else:
        print("List is Empty!")


def get_author_links() -> list:
    author_links_set = set()
    get_author_links = soup.find_all('a', string="(about)")
    for lk in get_author_links:
        author_links_set.add(BASE_URL + lk["href"])
    # print(list(author_links_set))
    return list(author_links_set)


def write_to_json(filename, data):
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
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
    # get_authors(get_author_links())
    get_author_links()
    # get_next_page()


if __name__ == '__main__':
    main()
