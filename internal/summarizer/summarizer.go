package summarizer

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"
)

type GeminiResponse struct {
	Candidates []struct {
		Content struct {
			Parts []struct {
				Text string `json:"text"`
			} `json:"parts"`
		} `json:"content"`
	} `json:"candidates"`
}

func Summarize(chunks []string) ([]string, int, string, error) {
	apiKey := os.Getenv("GOOGLE_API_KEY")
	if apiKey == "" {
		return nil, 0, "", fmt.Errorf("GOOGLE_API_KEY not set")
	}

	if len(chunks) <= 1 {
		return summarizeSingleChunk(chunks[0], apiKey)
	}

	var initialResponse strings.Builder
	for i, chunk := range chunks {
		prompt := fmt.Sprintf(`
        Resumir el fragmento de un artículo publicado en el Boletín Oficial de Argentina y responder en español.
        Tener en cuenta que es el trozo %d de %d trozos.
        El resultado final tendrá 140 caracteres máximo, no decorar con caracteres especiales ni hashtags, solo texto simple.
        Review: ####%s####
        `, i+1, len(chunks)+1, chunk)

		resp, err := callGeminiAPI(prompt, apiKey)
		if err != nil {
			return nil, 0, "", err
		}
		initialResponse.WriteString(resp)
	}

	prompt := fmt.Sprintf(`
    Resumir el siguiente texto de manera formal en 140 caracteres máximo y responder en español,
    no decorar con caracteres especiales ni hashtags, solo texto simple.
    Texto: ####%s####
    `, initialResponse.String())

	return summarizeSingleChunk(prompt, apiKey)
}

func summarizeSingleChunk(prompt, apiKey string) ([]string, int, string, error) {
	resp, err := callGeminiAPI(prompt, apiKey)
	if err != nil {
		return nil, 0, "", err
	}
	if resp == "" {
		return nil, 0, "", fmt.Errorf("empty response from Gemini API")
	}
	return []string{}, 0, resp, nil
}

func callGeminiAPI(prompt, apiKey string) (string, error) {
	url := "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + apiKey
	body := map[string]interface{}{"contents": []map[string]interface{}{{"parts": []map[string]string{{"text": prompt}}}}}

	data, err := json.Marshal(body)
	if err != nil {
		return "", err
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(data))
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	var geminiResp GeminiResponse
	if err := json.NewDecoder(resp.Body).Decode(&geminiResp); err != nil {
		return "", err
	}

	if len(geminiResp.Candidates) == 0 || len(geminiResp.Candidates[0].Content.Parts) == 0 {
		return "", fmt.Errorf("no valid response from Gemini API")
	}

	return geminiResp.Candidates[0].Content.Parts[0].Text, nil
}
