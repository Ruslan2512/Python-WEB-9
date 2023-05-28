import json

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import lxml

base_url = 'https://quotes.toscrape.com'
urls_list = [base_url]


def recursion_parse_pages(url):
    response_pages = requests.get(url)
    soup_pages = BeautifulSoup(response_pages.text, 'lxml')
    content_pages = soup_pages.select('li[class=next] a')
    page = urljoin(url, content_pages[0]["href"][0: -1])
    parsed = urlparse(page)
    if bool(parsed.netloc) and bool(parsed.scheme) is True:
        try:
            recursion_parse_pages(page)
            urls_list.append(page)
        except IndexError:
            urls_list.append(page)
    return urls_list


def parse_quotes(list_of_urls):
    quotes_list = []
    for url in list_of_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')
        tags = soup.find_all('div', class_='tags')
        for i in range(0, len(quotes)):
            name_author = authors[i].text
            name_quote = quotes[i].text
            tagsforquote = tags[i].find_all('a', class_='tag')
            tags_list = []
            for tag in tagsforquote:
                tags_list.append(tag.text)

            quotes_dict = {
                "tags": tags_list,
                "author": name_author,
                "quote": name_quote
                }

            quotes_list.append(quotes_dict)

    return quotes_list


def parse_authors(list_of_urls):
    authors_list = []
    for url in list_of_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        about_author = soup.select('div[class=quote] span a')
        for i in about_author:
            about_page = urljoin(base_url, i["href"])
            response_author = requests.get(about_page)
            soup_author = BeautifulSoup(response_author.text, 'lxml')

            fullname_author = soup_author.find_all('h3', class_='author-title')
            born_date_author = soup_author.find_all('span', class_='author-born-date')
            born_location_author = soup_author.find_all('span', class_='author-born-location')
            description_author = soup_author.find_all('div', class_='author-description')

            fullname = fullname_author[0].text.replace('\n    ', '')
            born_date = born_date_author[0].text
            born_location = born_location_author[0].text
            description = description_author[0].text.replace('\n        ', '').replace('    \n    ', '')

            authors_dict = {
                "fullname": fullname,
                "born_date": born_date,
                "born_location": born_location,
                "description": description
                }

            authors_list.append(authors_dict)

    return authors_list


def get_quoters(list_of_quotes):
    with open('quotes.json', 'a') as qj:
        json.dump(list_of_quotes, qj)
        qj.close()


def get_authors(list_of_authors):
    with open('authors.json', 'a') as qj:
        json.dump(list_of_authors, qj)
        qj.close()


if __name__ == '__main__':
    recursion_parse_pages(base_url)
    pq = parse_quotes(urls_list)
    pa = parse_authors(urls_list)
    get_quoters(pq)
    get_authors(pa)

