from bs4 import BeautifulSoup
import requests
import logging

BASE_URL = 'https://www.boletinoficial.gob.ar'

def today_urls():
    """
    Returns a list of ids that correspond
    to that day's publications.
    """
    articles_url = f'{BASE_URL}/seccion/primera'

    try:
        page = requests.get(articles_url)
        page.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(f"Error occurred: {err}")
        return [], None

    soup = BeautifulSoup(page.content, "html.parser")
    body = soup.find(id='avisosSeccionDiv')

    urls = [
        f'{BASE_URL}{a["href"]}'
        for a in body.find_all("a", href=True)
    ]

    return urls, page.status_code

def scrape_article(article_url):
    """
    Scrapes article from Boletin Oficial.
    Returns Type, Content and Date.
    """
    try:
        page = requests.get(article_url)
        page.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(f"Error occurred: {err}")
        return None, None, None, None

    soup = BeautifulSoup(page.content, "html.parser")

    area = soup.find(id="tituloDetalleAviso").find("h1").text

    article_type = soup.find(class_="puntero first-section").text
    
    content = soup.find(id="cuerpoDetalleAviso").text

    return article_type, area, content, page.status_code