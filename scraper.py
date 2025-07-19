# scraper.py

import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_chapter(url, output_dir="scraped_data"):
    # Make sure output folder exists
    os.makedirs(output_dir, exist_ok=True)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract title and text
    title = soup.find('h1').get_text(strip=True)
    paragraphs = soup.select('div#mw-content-text > div.mw-parser-output > p')
    chapter_text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

    # Save as raw txt
    with open(os.path.join(output_dir, 'chapter1_raw.txt'), 'w', encoding='utf-8') as f:
        f.write(chapter_text)

    # Save as JSON
    chapter_data = {
        "title": title,
        "url": url,
        "content": chapter_text
    }

    with open(os.path.join(output_dir, 'chapter_1.json'), 'w', encoding='utf-8') as f:
        json.dump(chapter_data, f, indent=4)

    print(f"✅ Chapter scraped and saved to {output_dir}/chapter_1.json")

if __name__ == "__main__":
    scrape_chapter("https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1")
