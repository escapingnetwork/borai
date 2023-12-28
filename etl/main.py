import json
import time
import datetime
import logging

from utils import scraper, loader, prompt, preprocesser

AREAS_OF_INTEREST = ["Resoluciones", "Leyes", "Decretos", "Disposiciones"]
RETRY_DELAY = 20

def process_url(url):
    """
    Process the given URL by scraping the article, preprocessing the content,
    summarizing it, and loading the publication to a JSON file.

    Args:
        url (str): The URL of the article to process.

    Returns:
        None
    """
    logging.info(f"Processing {url}")
    type, area, content, _ = scraper.scrape_article(url)

    if type not in AREAS_OF_INTEREST:
        logging.info(f"Area: {area} not in Areas Of Interest.")
        return

    chunks = preprocesser.chop(content)
    date = datetime.date.today()

    try:
        tags, score, summary = prompt.summarize(chunks)
    except Exception as error:
        logging.error(f"{error}, Retrying in {RETRY_DELAY}s...")
        time.sleep(RETRY_DELAY)
        tags, score, summary = prompt.summarize(chunks)

    publication = {
        'date': str(date),
        'area': area,
        'url': url,
        'type': type,
        'summary': summary,
        'score': score
    }

    logging.info('Publication Created')
    logging.info(publication)

    loader.json_loader(publication)
    logging.info("Loaded to json")

def main():
    urls, _ = scraper.today_urls()
    urls = list(dict.fromkeys(urls))
    logging.info(f"{len(urls)} Publications found.")

    for i, url in enumerate(urls):
        logging.info(f"Publication {i+1} of {len(urls)}")
        process_url(url)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()