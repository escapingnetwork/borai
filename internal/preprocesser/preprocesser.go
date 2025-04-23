package preprocesser

import (
	"borai/internal/loader"
	"time"
)

func Chop(text string, chunkSize, overlap int) []string {

	var chunks []string
	for i := 0; i < len(text); i += (chunkSize - overlap) * 4 {
		end := i + chunkSize*4
		if end > len(text) {
			end = len(text)
		}
		chunks = append(chunks, text[i:end])
	}
	return chunks

}

func TransformDate(date, inputFormat, outputFormat string) (string, error) {
	t, err := time.Parse(inputFormat, date)
	if err != nil {
		return "", err
	}
	return t.Format(outputFormat), nil
}

func Sort(data []loader.Publication, date time.Time) []loader.Publication {
	var sorted []loader.Publication
	dateStr := date.Format("2006-01-02")
	for _, p := range data {
		if p.Date == dateStr {
			sorted = append(sorted, p)
		}
	}

	return sorted

}
