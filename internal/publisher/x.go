package publisher

import (
	"bytes"
	"fmt"
	"os"
	"strconv"
	"text/template"

	"github.com/dghubble/go-twitter/twitter"
	"github.com/dghubble/oauth1"
)

func PublishX(tmpl *template.Template, data interface{}, inReplyTo *string) (string, error) {
	bearer := os.Getenv("X_BEARER")
	apiKey := os.Getenv("X_API_KEY")
	apiSecret := os.Getenv("X_API_KEY_SECRET")
	accessToken := os.Getenv("X_ACCESS_TOKEN")
	accessTokenSecret := os.Getenv("X_ACCESS_TOKEN_SECRET")
	if bearer == "" || apiKey == "" || apiSecret == "" || accessToken == "" || accessTokenSecret == "" {
		return "", fmt.Errorf("X API credentials not set")
	}

	config := oauth1.NewConfig(apiKey, apiSecret)
	token := oauth1.NewToken(accessToken, accessTokenSecret)
	httpClient := config.Client(oauth1.NoContext, token)
	client := twitter.NewClient(httpClient)

	var buf bytes.Buffer
	if err := tmpl.Execute(&buf, data); err != nil {
		return "", err
	}

	tweetParams := &twitter.StatusUpdateParams{}
	if inReplyTo != nil {
		inReplyToID, err := strconv.ParseInt(*inReplyTo, 10, 64)
		if err != nil {
			return "", fmt.Errorf("invalid inReplyTo ID: %v", err)
		}
		tweetParams.InReplyToStatusID = inReplyToID
	}

	tweet, _, err := client.Statuses.Update(buf.String(), tweetParams)
	if err != nil {
		return "", err
	}
	return tweet.IDStr, nil
}
