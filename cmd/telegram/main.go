package main

import (
	"fmt"
	"log"
	"sync"
	"text/template"
	"time"

	"borai/internal/loader"
	"borai/internal/preprocesser"
	"borai/internal/publisher"
)

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

	tmpl, err := template.ParseGlob("templates/*.j2")
	if err != nil {
		log.Fatalf("Failed to parse templates: %v", err)
	}

	todayStr := today.Format("2006-01-02")
	var wg sync.WaitGroup

	// Send resume
	resumeTmpl := tmpl.Lookup("notePost.j2")
	if err := publisher.PublishTelegram(resumeTmpl, map[string]interface{}{"today": todayStr}, &wg); err != nil {
		log.Printf("Failed to publish resume: %v", err)
	}

	// Send posts by type
	types := make(map[string]bool)
	for _, p := range data {
		types[p.Type] = true
	}

	for t := range types {
		// Publish header
		headTmpl := tmpl.Lookup("head.j2")
		if err := publisher.PublishTelegram(headTmpl, map[string]interface{}{"today": todayStr, "type": t}, &wg); err != nil {
			log.Printf("Failed to publish header for %s: %v", t, err)
		}

		// Publish posts
		for _, p := range data {
			if p.Type == t {
				postTmpl := tmpl.Lookup("post.j2")
				if err := publisher.PublishTelegram(postTmpl, map[string]interface{}{"publication": p, "today": todayStr, "type": t}, &wg); err != nil {
					log.Printf("Failed to publish post: %v", err)
				}
			}
		}
	}

	wg.Wait()
}
