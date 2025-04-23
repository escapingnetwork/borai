package main

import (
	"fmt"
	"log"
	"text/template"
	"time"

	"borai/internal/loader"
	"borai/internal/preprocesser"
	"borai/internal/publisher"
)

const tweetMaxLength = 327

func main() {
	today := time.Now()
	data, err := loader.LoadPublications(today)
	if err != nil {
		log.Fatalf("Failed to load data: %v", err)
	}

	data = preprocesser.Sort(data, today)
	if len(data) == 0 {
		fmt.Println("No publications to publish")
		return
	}

	for _, p := range data {
		if len(p.Summary) > 280 {
			log.Printf("Summary too long for %s: %d chars", p.URL, len(p.Summary))
			return
		}
	}

	tmpl, err := template.ParseGlob("templates/*.j2")
	if err != nil {
		log.Fatalf("Failed to parse templates: %v", err)
	}

	todayStr := today.Format("2006-01-02")
	types := make(map[string]bool)
	for _, p := range data {
		types[p.Type] = true
	}

	for t := range types {
		headTmpl := tmpl.Lookup("head.j2")
		tweetID, err := publisher.PublishX(headTmpl, map[string]interface{}{"today": todayStr, "type": t}, nil)
		if err != nil {
			log.Printf("Failed to publish header for %s: %v", t, err)
			continue
		}

		for _, p := range data {
			if p.Type == t {
				postTmpl := tmpl.Lookup("post.j2")
				if len(p.Summary) > tweetMaxLength {
					areaTmpl := tmpl.Lookup("area.j2")
					newTweetID, err := publisher.PublishX(areaTmpl, map[string]interface{}{"publication": p, "today": todayStr, "type": t}, &tweetID)
					if err != nil {
						log.Printf("Failed to publish area for %s: %v", p.URL, err)
						continue
					}

					summaryTmpl := tmpl.Lookup("summary.j2")
					newTweetID, err = publisher.PublishX(summaryTmpl, map[string]interface{}{"publication": p, "today": todayStr, "type": t}, &newTweetID)
					if err != nil {
						log.Printf("Failed to publish summary for %s: %v", p.URL, err)
						continue
					}
					tweetID = newTweetID
				} else {
					newTweetID, err := publisher.PublishX(postTmpl, map[string]interface{}{"publication": p, "today": todayStr, "type": t}, &tweetID)
					if err != nil {
						log.Printf("Failed to publish post for %s: %v", p.URL, err)
						continue
					}
					tweetID = newTweetID
				}
			}
		}
	}
}
