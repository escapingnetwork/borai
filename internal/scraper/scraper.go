package scraper

import (
	"fmt"
	"net/http"
	"strings"

	"github.com/PuerkitoBio/goquery"
	"github.com/gocolly/colly/v2"
)

func TodayURLs() ([]string, error) {
	var urls []string
	c := colly.NewCollector()

	c.OnHTML("#avisosSeccionDiv a[href]", func(e *colly.HTMLElement) {
		url := "https://www.boletinoficial.gob.ar" + strings.Split(e.Attr("href"), "?")[0]
		urls = append(urls, url)
	})

	err := c.Visit("https://www.boletinoficial.gob.ar/seccion/primera")
	if err != nil {
		return nil, err
	}

	// Remove duplicates
	seen := make(map[string]bool)
	var unique []string
	for _, url := range urls {
		if !seen[url] {
			seen[url] = true
			unique = append(unique, url)
		}
	}
	return unique, nil
}

func ScrapeArticle(url string) (string, string, string, error) {
	resp, err := http.Get(url)
	if err != nil {
		return "", "", "", err
	}
	defer resp.Body.Close()

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		return "", "", "", err
	}

	area := strings.TrimSpace(doc.Find("#tituloDetalleAviso h1").Text())
	// Clean articleType by replacing non-breaking spaces and trimming
	articleType := strings.TrimSpace(strings.ReplaceAll(doc.Find(".puntero.first-section").Text(), "\u00a0", " "))
	content := strings.TrimSpace(doc.Find("#cuerpoDetalleAviso").Text())

	if area == "" || articleType == "" || content == "" {
		return "", "", "", fmt.Errorf("failed to scrape required fields from %s", url)
	}

	return articleType, area, content, nil
}
