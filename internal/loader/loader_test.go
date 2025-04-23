package loader

import (
	"os"
	"reflect"
	"testing"
	"time"
)

func TestSaveAndLoadPublication(t *testing.T) {
	tempDir := "test_data"
	defer os.RemoveAll(tempDir)

	date, _ := time.Parse("2006-01-02", "2023-12-11")
	pub := Publication{
		Date:    "2023-12-11",
		Area:    "TEST_AREA",
		URL:     "https://test.com",
		Type:    "Decretos",
		Summary: "Test summary",
	}

	if err := SavePublication(pub); err != nil {
		t.Fatalf("SavePublication failed: %v", err)
	}

	data, err := LoadPublications(date)
	if err != nil {
		t.Fatalf("LoadPublications failed: %v", err)
	}

	if len(data) != 1 {
		t.Fatalf("Expected 1 publication, got %d", len(data))
	}

	if !reflect.DeepEqual(data[0], pub) {
		t.Errorf("Expected %+v, got %+v", pub, data[0])
	}

}

func TestGenerateMarkdown(t *testing.T) {
	tempDir := "test_summaries"
	defer os.RemoveAll(tempDir)

	date, _ := time.Parse("2006-01-02", "2023-12-11")
	data := []Publication{
		{
			Date:    "2023-12-11",
			Area:    "TEST_AREA",
			URL:     "https://test.com",
			Type:    "Decretos",
			Summary: "Test summary",
		},
	}

	if err := GenerateMarkdown(data, date); err != nil {
		t.Fatalf("GenerateMarkdown failed: %v", err)
	}

	content, err := os.ReadFile("summaries/2023-12-11.md")
	if err != nil {
		t.Fatalf("Failed to read Markdown file: %v", err)
	}

	expected := `# Boletín Oficial Summary - 2023-12-11


## Decretos

- **Area**: TEST_AREA
  - **Summary**: Test summary
  - **URL**: https://test.com \`
	if string(content) != expected {
		t.Errorf("Expected Markdown:\\n%s\\nGot:\\n%s", expected, string(content))
	}
}
