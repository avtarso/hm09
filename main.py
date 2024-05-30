import requests
from bs4 import BeautifulSoup
from time import sleep
import json
import logging
import random
from typing import List, Dict, Optional

def clean_data(dict_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [
        {key: value.strip() if isinstance(value, str) else value for key, value in item.items()}
        for item in dict_list
    ]

def fetch_page(url: str) -> Optional[BeautifulSoup]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'lxml')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

def get_authors_links(soup: BeautifulSoup) -> Dict[str, str]:
    return {
        author.text: author.find_next("a")["href"]
        for author in soup.find_all('small', class_='author')
    }

def get_quotes(soup: BeautifulSoup) -> List[Dict[str, str]]:
    return [
        {
            "tags": get_tags(quote.find('meta', class_='keywords')["content"]),
            "author": quote.find('small', class_='author').text,
            "quote": quote.find('span', class_='text').text
        }
        for quote in soup.find_all('div', class_='quote')
    ]

def get_tags(tags_string: str) -> List[str]:
    return tags_string.split(',')

def get_next_page(soup: BeautifulSoup, base_url: str) -> Optional[str]:
    next_link_block = soup.find('li', class_='next')
    if next_link_block:
        next_link = next_link_block.find('a')
        if next_link:
            return base_url + next_link["href"]
    return None

def get_author_info(base_url: str, author: str, link: str) -> Optional[Dict[str, str]]:
    logging.info(f"Getting info for {author}")
    soup = fetch_page(base_url + link)
    if soup:
        return {
            "fullname": soup.find('h3', class_='author-title').text.strip(),
            "born_date": soup.find('span', class_='author-born-date').text.strip(),
            "born_location": soup.find('span', class_='author-born-location').text.strip(),
            "description": soup.find('div', class_="author-description").text.strip()
        }
    return None

def write_data(output_file: str, data: List[Dict[str, str]]) -> None:
    with open(output_file, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    logging.info(f"Data successfully written to {output_file}")

def random_sleep():
    sleep(random.uniform(1, 3))

def get_data(base_url: str, start_page: str, output_authors_file: str, output_quotes_file: str) -> None:
    url = start_page
    authors_links = {}
    quotes_list = []
    authors_info = []

    while url:
        soup = fetch_page(url)
        if not soup:
            break

        authors_links.update(get_authors_links(soup))
        quotes_list.extend(get_quotes(soup))
        url = get_next_page(soup, base_url)
        if url:
            logging.info(f"Going to scrape next URL --> {url}")
            random_sleep()

    for author, link in authors_links.items():
        author_info = get_author_info(base_url, author, link)
        if author_info:
            authors_info.append(author_info)
            random_sleep()

    write_data(output_authors_file, clean_data(authors_info))
    write_data(output_quotes_file, clean_data(quotes_list))


if __name__ == '__main__':
    output_authors_file = "authors.json"
    output_quotes_file = "quotes.json"
    domen = "https://quotes.toscrape.com/"
    start_page = "https://quotes.toscrape.com/"

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    get_data(domen, start_page, output_authors_file, output_quotes_file)
