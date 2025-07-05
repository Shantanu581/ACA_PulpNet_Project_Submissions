import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://voxiitk.com"
CATEGORY_URL = BASE_URL + "/category/editorials-and-opinions/"
OUTPUT_FILE = "editorials_and_opinions_post.json"

def get_soup(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    }
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def extract_post_links(soup):
    return [a['href'] for a in soup.select("h2.entry-title.entry-title-big a")]

def extract_post_data(url):
    soup = get_soup(url)
    data = {}
    # Title
    title_tag = soup.find("h1", class_="entry-title.entry-title-large")
    if not title_tag:
     title_tag = soup.find("h1", class_="entry-title")
    data["title"] = title_tag.get_text(strip=True) if title_tag else ""
    # Date
    time_tag = soup.select_one(
        'div.entry-meta-wrapper div.entry-meta.entry-date.posted-on a time.entry-date.published'
    )
    if time_tag:
        data["date"] = time_tag.get("datetime", "")
        data["date_text"] = time_tag.get_text(strip=True)
    else:
        data["date"] = ""
        data["date_text"] = ""
    # Author
    author_text = ""
    for div in soup.find_all("div", class_="elementor-widget-container"):
        for p in div.find_all("p"):
            if "written by" in p.get_text(strip=True).lower():
                author_text = p.get_text(strip=True)
                break
        if author_text:
            break
    authors = []
    if "written by" in author_text.lower():
        if "–" in author_text:
            author_names = author_text.split("–", 1)[-1].strip()
        else:
            author_names = author_text.split("-", 1)[-1].strip()
        authors = [name.strip() for name in author_names.split(",") if name.strip()]
    data["authors"] = authors
    # Content
    content_div = soup.find("div", class_="entry-content")
    if content_div:
        paragraphs = [p.get_text(strip=True) for p in content_div.find_all("p")]
        data["content"] = paragraphs
    else:
        data["content"] = []
    return data

def get_next_page_url(soup):
    for a in soup.find_all("a", href=True):
        span = a.find("span", class_="nav-prev-text title")
        if span and "older articles" in span.get_text(strip=True).lower():
            return a['href']
    return None


def main():
    all_posts = []
    page_url = CATEGORY_URL
    page_num = 1

    while page_url:
        print(f"Processing page: {page_url}")
        soup = get_soup(page_url)
        post_links = extract_post_links(soup)
        for link in post_links:
            print(f"  Scraping post: {link}")
            post_data = extract_post_data(link)
            all_posts.append(post_data)
            time.sleep(1)
        page_url = get_next_page_url(soup)
        page_num += 1
        time.sleep(2)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=2, ensure_ascii=False)
    print(f"Scraping complete. Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
