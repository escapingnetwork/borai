package preprocesser

import (
	"borai/internal/loader"
	"testing"
	"time"
)

func TestTransformDate(t *testing.T) {
	date := "31/01/1991"
	expected := "1991-01-31"
	result, err := TransformDate(date, "02/01/2006", "2006-01-02")
	if err != nil {
		t.Fatalf("TransformDate failed: %v", err)
	}
	if result != expected {
		t.Errorf("Expected %s, got %s", expected, result)
	}
}

func TestChop(t *testing.T) {
	text := "This is a test string with more than enough characters to be chunked."
	chunks := Chop(text, 10, 2)
	if len(chunks) < 2 {
		t.Errorf("Expected multiple chunks, got %d", len(chunks))
	}
}

func TestRankAndSort(t *testing.T) {
	data := []loader.Publication{
		{Date: "2023-12-11"},
		{Date: "2023-12-11"},
		{Date: "2023-12-10"},
		{Date: "2023-12-11"},
	}
	date, _ := time.Parse("2006-01-02", "2023-12-11")
	result := Sort(data, date)
	if len(result) != 0 {
		t.Errorf("Expected 0 publications, got %d", len(result))
	}
}
