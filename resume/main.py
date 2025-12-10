import json
import time
import datetime


from utils import scraper, loader, prompt, preprocesser


areas_of_interest = ["Resoluciones", "Resoluciones Generales", "Resoluciones Conjuntas","Tratados Y Convenios Internacionales", "Leyes", "Decretos", "Disposiciones"]
def main():
    ## To execute manualy on a particular date replace urls with a list of urls from that date
    urls, _ = scraper.today_urls()
    #start = 335679
    #end = 335764
    #urls = [
    #    f"https://www.boletinoficial.gob.ar/detalleAviso/primera/{numero}/20251209"
    #    for numero in range(start, end + 1)
    #]
    print(f"{len(urls)} Publications found.")
    print('***************')

    for i, url in enumerate(urls):
        print(f"Publication {i+1} of {len(urls)}")
        type, area, content, _ = scraper.scrape_article(url)
        print('Completed Scraping')

        if type  in areas_of_interest:
            chunks = preprocesser.chop(content)
            date = datetime.date.today()
            #date = datetime.date(2025, 12, 9)
            print('Completed Preprocessing')

            try:
                tags, score, summary = prompt.summarize(chunks)
            except () as error:
                print(error, "\n Retrying in 20s...")
                time.sleep(20)
                tags, score, summary = prompt.summarize(chunks)

            print('Completed Extraction')

            if len(summary) > 0:

                publication = {
                    'date': str(date),
                    'area': area,
                    'url': url,
                    'type': type,
                    'summary': summary,
                    'score': score
                }

                print('Publication Created')
                print(publication)

                loader.json_loader(publication)
                print("Loaded to json")
        else:
            print(f"Area: {area} not in Areas Of Interest.")
        print('***************')

if __name__ == "__main__":
    main()
