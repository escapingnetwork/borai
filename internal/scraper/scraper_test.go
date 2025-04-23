package scraper

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestTodayURLs(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte(`<div id="avisosSeccionDiv"> <a href="/detalleAviso/primera/1">Link 1</a> <a href="/detalleAviso/primera/2">Link 2</a> <a href="/detalleAviso/primera/1">Link 1</a> </div>`))
	}))
	defer server.Close()

	urls, err := TodayURLs()
	if err != nil {
		t.Fatalf("TodayURLs failed: %v", err)
	}
	if len(urls) != 2 {
		t.Errorf("Expected 2 unique URLs, got %d", len(urls))
	}

}

func TestScrapeArticle(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte(`<div id="tituloDetalleAviso"><h1>Test Area</h1></div> <div class="puntero first-section">Decretos&nbsp;</div> <div id="cuerpoDetalleAviso">Test Content</div>`))
	}))
	defer server.Close()

	articleType, area, content, err := ScrapeArticle(server.URL)
	if err != nil {
		t.Fatalf("ScrapeArticle failed: %v", err)
	}
	if articleType != "Decretos" {
		t.Errorf("Expected articleType 'Decretos', got '%s'", articleType)
	}
	if area != "Test Area" {
		t.Errorf("Expected area 'Test Area', got '%s'", area)
	}
	if content != "Test Content" {
		t.Errorf("Expected content 'Test Content', got '%s'", content)
	}

}

func TestScrapeArticleWithMultipleNBSP(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte(`<div id="tituloDetalleAviso"><h1>Test Area</h1></div> <div class="puntero first-section">Decretos&nbsp;&nbsp;</div> <div id="cuerpoDetalleAviso">Test Content</div>`))
	}))
	defer server.Close()

	articleType, _, _, err := ScrapeArticle(server.URL)
	if err != nil {
		t.Fatalf("ScrapeArticle failed: %v", err)
	}
	if articleType != "Decretos" {
		t.Errorf("Expected articleType 'Decretos', got '%s'", articleType)
	}

}
