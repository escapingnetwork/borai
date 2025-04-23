package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"os"
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
	types := make(map[string]bool)
	for _, p := range data {
		types[p.Type] = true
	}

	// Publish to Urbit
	urbitTmpl := tmpl.Lookup("note.j2")
	var buf bytes.Buffer
	if err := urbitTmpl.Execute(&buf, map[string]interface{}{
		"results": data,
		"today":   todayStr,
		"types":   types,
		"nest":    fmt.Sprintf("diary/~%s/%s", os.Getenv("URBIT_SHIP"), os.Getenv("URBIT_DIARY")),
		"ship":    fmt.Sprintf("~%s", os.Getenv("URBIT_SHIP")),
		"time":    time.Now().UnixMilli(),
	}); err != nil {
		log.Fatalf("Failed to render Urbit template: %v", err)
	}

	var note map[string]interface{}
	if err := json.Unmarshal(buf.Bytes(), &note); err != nil {
		log.Fatalf("Failed to parse note JSON: %v", err)
	}

	if err := publisher.PublishUrbit(note); err != nil {
		log.Printf("Failed to publish to Urbit: %v", err)
	}

	// Publish to X
	resumeTmpl := tmpl.Lookup("notePost.j2")
	if _, err := publisher.PublishX(resumeTmpl, map[string]interface{}{"today": todayStr}, nil); err != nil {
		log.Printf("Failed to publish resume to X: %v", err)
	}
}
