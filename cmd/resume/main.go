package main

import (
	"fmt"
	"log"
	"time"

	"borai/internal/loader"
	"borai/internal/preprocesser"
	"borai/internal/scraper"
	"borai/internal/summarizer"
)

var areasOfInterest = []string{
	"Resoluciones", "Resoluciones Generales", "Resoluciones Conjuntas",
	"Tratados Y Convenios Internacionales", "Leyes", "Decretos", "Disposiciones",
}

func main() {
	urls, err := scraper.TodayURLs()
	if err != nil {
		log.Fatalf("Failed to fetch URLs: %v", err)
	}
	fmt.Printf("%d Publications found.\n***************\n", len(urls))

	today := time.Now()
	var publications []loader.Publication

	for i, url := range urls {
		fmt.Printf("Publication %d of %d\n", i+1, len(urls))
		articleType, area, content, err := scraper.ScrapeArticle(url)
		if err != nil {
			log.Printf("Failed to scrape %s: %v", url, err)
			continue
		}
		fmt.Println("Completed Scraping")

		if contains(areasOfInterest, articleType) {
			chunks := preprocesser.Chop(content, 4000, 200)
			date := today.Format("2006-01-02")
			fmt.Println("Completed Preprocessing")

			_, _, summary, err := summarizer.Summarize(chunks)
			if err != nil {
				log.Printf("Failed to summarize %s: %v", url, err)
				time.Sleep(20 * time.Second)
				_, _, summary, err = summarizer.Summarize(chunks)
				if err != nil {
					log.Printf("Retry failed for %s: %v", url, err)
					continue
				}
			}
			fmt.Println("Completed Extraction")

			if len(summary) > 0 {
				publication := loader.Publication{
					Date:    date,
					Area:    area,
					URL:     url,
					Type:    articleType,
					Summary: summary,
				}
				fmt.Printf("Publication Created\n%+v\n", publication)

				if err := loader.SavePublication(publication); err != nil {
					log.Printf("Failed to save publication: %v", err)
				} else {
					fmt.Println("Loaded to json")
					publications = append(publications, publication)
				}
			}
		} else {
			fmt.Printf("Area: %s not in Areas Of Interest.\n", area)
		}
		fmt.Println("***************")
	}

	if len(publications) > 0 {
		if err := loader.GenerateMarkdown(publications, today); err != nil {
			log.Printf("Failed to generate Markdown: %v", err)
		} else {
			fmt.Println("Generated Markdown summary")
		}
	}
}

func contains(slice []string, item string) bool {
	for _, s := range slice {
		if s == item {
			return true
		}
	}
	return false
}
