package publisher

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

func PublishUrbit(note map[string]interface{}) error {
	shipURL := os.Getenv("URBIT_SHIP_URL")
	shipCode := os.Getenv("URBIT_SHIP_CODE")
	shipName := os.Getenv("URBIT_SHIP")
	if shipURL == "" || shipCode == "" || shipName == "" {
		return fmt.Errorf("URBIT_SHIP_URL, URBIT_SHIP_CODE, or URBIT_SHIP not set")
	}

	data, err := json.Marshal(note)
	if err != nil {
		return err
	}

	req, err := http.NewRequest("POST", shipURL+"/api/channels/channel-action", bytes.NewBuffer(data))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")
	req.SetBasicAuth(shipName, shipCode)

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("Urbit API returned status: %d", resp.StatusCode)
	}
	return nil
}