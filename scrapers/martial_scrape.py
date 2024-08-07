import requests
from bs4 import BeautifulSoup
import os

base_url = "https://fast.novelupdates.net/book/martial-god-regressed-to-level-2/"
start_chapter = "chapter-1"

def scrape_chapter(chapter_url):
    response = requests.get(base_url + chapter_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Use the select element's option text as a title (if present)
    title_tag = soup.find('select', class_='single-chapter-select')
    if title_tag:
        title = title_tag.find('option', value=chapter_url).text.strip()
    else:
        title = "Chapter " + chapter_url

    # Extract the content from the div with class 'text-left'
    content_div = soup.find('div', class_='chr-c')
    if not content_div:
        print(f"Error: Content not found for {chapter_url}")
        return None, None

    content_html = content_div.prettify()

    # Save the chapter as an HTML file
    chapter_filename = chapter_url.replace("/", "_") + ".html"
    with open(chapter_filename, "w", encoding='utf-8') as file:
        file.write(f"<html><head><title>{title}</title></head><body>")
        file.write(f"<h1>{title}</h1>")
        file.write(content_html)
        file.write("</body></html>")

    return chapter_filename, soup

def scrape_novel(start_chapter):
    chapter_files = []
    next_chapter_url = start_chapter

    while next_chapter_url:
        chapter_filename, soup = scrape_chapter(next_chapter_url)
        if chapter_filename:
            chapter_files.append(chapter_filename)
        else:
            print(f"Skipping chapter due to missing elements: {next_chapter_url}")

        # url of next chapter
        next_button = soup.find('div', class_='btn-group')
        if next_button and next_button.find('a'):
            next_chapter_url = next_button.find('a', id="next_chap").get('href').split(base_url)[-1]
            print("hello: " + next_chapter_url)
        else:
            next_chapter_url = None
            print(next_chapter_url)

    return chapter_files

if __name__ == "__main__":
    os.makedirs("martial_god", exist_ok=True)
    os.chdir("martial_god")
    chapter_files = scrape_novel(start_chapter)
    print("Scraping completed. Chapter files:", chapter_files)
