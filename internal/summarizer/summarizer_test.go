package summarizer

import (
	"net/http"
	"net/http/httptest"
	"os"
	"testing"
)

func TestSummarize(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte(`{
			"candidates": [{
				"content": {
					"parts": [{"text": "Test summary"}]
				}
			}]
		}`))
	}))
	defer server.Close()

	os.Setenv("GOOGLE_API_KEY", "test-key")
	defer os.Unsetenv("GOOGLE_API_KEY")

	_, _, summary, err := Summarize([]string{"Test content"})
	if err != nil {
		t.Fatalf("Summarize failed: %v", err)
	}
	if summary != "Test summary" {
		t.Errorf("Expected summary 'Test summary', got '%s'", summary)
	}
}
