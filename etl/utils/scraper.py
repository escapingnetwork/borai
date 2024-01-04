from bs4 import BeautifulSoup
import requests

def today_urls():
    """
    Returns a list of ids that correspond
    to that day's publications.
    """
    base_url = 'https://www.boletinoficial.gob.ar'
    articles_url = base_url + '/seccion/primera'

    page = requests.get(articles_url)
    status = page.status_code

    soup = BeautifulSoup(page.content, "html.parser")
    body = soup.find(id='avisosSeccionDiv')

    urls = []

    for a in body.find_all("a", href=True):
        url = base_url + remove_query_params(a['href'])
        urls.append(url)
    


    urls = list(dict.fromkeys(urls))
    return urls, status

def scrape_article(article_url):
    """
    Scrapes article from Boletin Oficial.
    Returns Type, Content and Date.
    """
    page = requests.get(article_url)
    status = page.status_code

    soup = BeautifulSoup(page.content, "html.parser")

    area = soup.find(id="tituloDetalleAviso")
    area = area.find("h1").text

    type = soup.find(class_="puntero first-section")
    type = type.text
    
    content = soup.find(id="cuerpoDetalleAviso").text

    return type, area, content, status

def remove_query_params(url):
    return url.split('?')[0]
