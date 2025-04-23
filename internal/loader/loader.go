package loader

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"text/template"
	"time"
)

type Publication struct {
	Date    string `json:"date"`
	Area    string `json:"area"`
	URL     string `json:"url"`
	Type    string `json:"type"`
	Summary string `json:"summary"`
}

func SavePublication(p Publication) error {
	date, err := time.Parse("2006-01-02", p.Date)
	if err != nil {
		return fmt.Errorf("invalid date format: %v", err)
	}

	dir := "data"
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("failed to create data directory: %v", err)
	}

	filename := filepath.Join(dir, date.Format("2006-01-02")+".json")
	var data []Publication

	file, err := os.Open(filename)
	if err == nil {
		if err := json.NewDecoder(file).Decode(&data); err != nil && err.Error() != "EOF" {
			file.Close()
			return fmt.Errorf("failed to decode existing JSON: %v", err)
		}
		file.Close()
	}

	data = append(data, p)
	file, err = os.Create(filename)
	if err != nil {
		return fmt.Errorf("failed to create JSON file: %v", err)
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	return encoder.Encode(data)
}

func LoadPublications(date time.Time) ([]Publication, error) {
	filename := filepath.Join("data", date.Format("2006-01-02")+".json")
	file, err := os.Open(filename)
	if err != nil {
		if os.IsNotExist(err) {
			return []Publication{}, nil
		}
		return nil, fmt.Errorf("failed to open JSON file: %v", err)
	}
	defer file.Close()

	var data []Publication
	if err := json.NewDecoder(file).Decode(&data); err != nil && err.Error() != "EOF" {
		return nil, fmt.Errorf("failed to decode JSON: %v", err)
	}
	return data, nil
}

func GenerateMarkdown(data []Publication, date time.Time) error {
	dir := "summaries"
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("failed to create summaries directory: %v", err)
	}

	filename := filepath.Join(dir, date.Format("2006-01-02")+".md")
	file, err := os.Create(filename)
	if err != nil {
		return fmt.Errorf("failed to create Markdown file: %v", err)
	}
	defer file.Close()

	tmpl := template.Must(template.New("markdown").Parse(`
# Boletín Oficial Summary - {{.Date}}

{{range $type, $pubs := .PublicationsByType}}## {{$type}}
{{range $pubs}}- **Area**: {{.Area}}
  - **Summary**: {{.Summary}}
  - **URL**: {{.URL}}
{{end}}
{{end}}`))

	typeByPubs := make(map[string][]Publication)
	for _, p := range data {
		typeByPubs[p.Type] = append(typeByPubs[p.Type], p)
	}

	return tmpl.Execute(file, struct {
		Date               string
		PublicationsByType map[string][]Publication
	}{
		Date:               date.Format("2006-01-02"),
		PublicationsByType: typeByPubs,
	})
}
