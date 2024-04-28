import json
from time import sleep

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com"
FILE_QUOTES = "quotes.json"
FILE_AUTHORS = "authors.json"


def start_parser():
    quotes_list = list()
    authors_list = list()
    print(authors_list)
    print(f"===>>> START PAGE {BASE_URL}")
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes_on_page = get_quotes_on_page(soup)
    quotes_list.extend(quotes_on_page)
    authors_link_list = get_links_authors(soup, authors_list)
    next_page = get_next_page(BASE_URL)
    while next_page is not None:
        sleep(0.5)
        print(f"===>>> START PAGE {next_page}")
        next_response = requests.get(next_page)
        next_soup = BeautifulSoup(next_response.text, 'lxml')
        quotes_on_page = get_quotes_on_page(next_soup)
        quotes_list.extend(quotes_on_page)
        authors_link_list = get_links_authors(next_soup, authors_link_list)
        sleep(0.5)
        next_page = get_next_page(next_page)
    else:
        print("THE END!")

    # with open("authors_link_list.txt", "w", encoding="utf-8") as fh:
    #     for link_elem in authors_link_list:
    #         fh.write(link_elem + "\n")
    with open("authors_link_list.txt") as fh:
        lines = fh.readlines()
    new_link_list = list()
    for link in lines:
        new_link = link.rstrip("\n")
        new_link_list.append(new_link)
    # print(len(new_link_list))
    # for idx in range(15):
    for lnk in new_link_list:
        # author_from_page = get_author(new_link_list[idx])
        author_from_page = get_author(lnk)
        authors_list.append(author_from_page)
    print(write_to_json(FILE_QUOTES, quotes_list))
    print(write_to_json(FILE_AUTHORS, authors_list))


def get_quotes_on_page(soup: BeautifulSoup) -> list[dict]:
    result_list = list()
    quotes_list = [quote.text for quote in soup.find_all('span', class_="text")]
    authors_list = [author.text for author in soup.find_all('small', class_="author")]
    tags_list = [tag.text.replace('Tags:', '').strip().split('\n') for tag in soup.find_all('div', class_="tags")]
    for quote, author, tags in zip(quotes_list, authors_list, tags_list):
        result_list.append(
            {
                "tags": tags,
                "author": author,
                "quote": quote
            }
        )
    return result_list


def get_author(link: str) -> list[dict]:
    sleep(1.2)
    print(f"===>>> START {link}")
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    fullname = soup.find('h3', class_="author-title").text
    born_date = soup.find('span', class_="author-born-date").text
    born_location = soup.find('span', class_="author-born-location").text
    description = soup.find('div', class_="author-description").text.strip()
    result = {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }
    return result


def get_links_authors(soup: BeautifulSoup, author_link_list: list) -> list:
    get_author_links = soup.find_all('a', string="(about)")
    for lk in get_author_links:
        if (BASE_URL + lk["href"]) not in author_link_list:
            author_link_list.append(BASE_URL + lk["href"])
    return author_link_list


def write_to_json(filename, data):
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    return f"Save {filename}"


def get_next_page(url: str) -> str | None:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    get_href = soup.select("li.next a")
    if get_href:
        get_href_link = get_href[0].attrs
        get_page_link = BASE_URL + get_href_link.get("href")
        return get_page_link
    else:
        return None


def main():
    start_parser()


if __name__ == '__main__':
    main()
