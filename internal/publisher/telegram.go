package publisher

import (
	"bytes"
	"fmt"
	"math/rand"
	"os"
	"sync"
	"text/template"
	"time"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func PublishTelegram(tmpl *template.Template, data interface{}, wg *sync.WaitGroup) error {
	botToken := os.Getenv("TELEGRAM_TOKEN")
	chatID := os.Getenv("TELEGRAM_CHANNEL")
	if botToken == "" || chatID == "" {
		return fmt.Errorf("TELEGRAM_TOKEN or TELEGRAM_CHANNEL not set")
	}

	bot, err := tgbotapi.NewBotAPI(botToken)
	if err != nil {
		return err
	}

	var buf bytes.Buffer
	if err := tmpl.Execute(&buf, data); err != nil {
		return err
	}

	message := buf.String()
	if len(message) > 4095 {
		for i := 0; i < len(message); i += 4095 {
			end := i + 4095
			if end > len(message) {
				end = len(message)
			}
			sendTelegramMessage(bot, chatID, message[i:end], wg)
		}
	} else {
		sendTelegramMessage(bot, chatID, message, wg)
	}
	return nil
}

func sendTelegramMessage(bot *tgbotapi.BotAPI, chatID, message string, wg *sync.WaitGroup) {
	if wg != nil {
		wg.Add(1)
	}
	go func() {
		if wg != nil {
			defer wg.Done()
		}
		for {
			msg := tgbotapi.NewMessageToChannel(chatID, message)
			_, err := bot.Send(msg)
			if err != nil {
				if e, ok := err.(tgbotapi.Error); ok && e.Code == 429 {
					time.Sleep(time.Duration(1+rand.Intn(59)) * time.Second)
					continue
				}
				fmt.Printf("Failed to send Telegram message: %v\n", err)
				return
			}
			fmt.Println("Telegram message sent successfully!")
			return
		}
	}()
}
