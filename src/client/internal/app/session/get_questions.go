package session

import (
	"context"
	"encoding/json/jsontext"
	"encoding/json/v2"
	"errors"
	"fmt"
	"io"
	"net/http"
	"time"

	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions"
)

type QuestionsGetMsg struct {
	Questions questions.Questions
}

const sessionPage = "session"

func extractJSONObjects(jsonList []byte) ([][]byte, error) {
	var rawSlice []jsontext.Value
	if err := json.Unmarshal(jsonList, &rawSlice); err != nil {
		return nil, err
	}

	if len(rawSlice) == 0 {
		return nil, errors.New("empty JSON array")
	}

	result := make([][]byte, len(rawSlice))
	for i, raw := range rawSlice {
		result[i] = []byte(raw)
	}

	return result, nil
}

func getQuestions(serverPort int) tea.Cmd {
	return func() tea.Msg {
		sessionConfigURL := fmt.Sprintf(
			"http://localhost:%d/%s",
			serverPort,
			sessionPage,
		)

		ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
		defer cancel()

		req, err := http.NewRequestWithContext(ctx, http.MethodGet, sessionConfigURL, nil)
		if err != nil {
			return app.ErrMsg(fmt.Errorf("failed to create request for %s: %w", sessionConfigURL, err))
		}

		client := &http.Client{}

		resp, err := client.Do(req)
		if err != nil {
			return app.ErrMsg(fmt.Errorf("failed to get questions from %s: %w", sessionConfigURL, err))
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			body, _ := io.ReadAll(resp.Body)

			return app.ErrMsg(
				fmt.Errorf(
					"failed to get questions from %s, status code: %d, response: %s",
					sessionConfigURL,
					resp.StatusCode,
					string(body),
				),
			)
		}

		// Read response from server
		body, err := io.ReadAll(resp.Body)
		if err != nil {
			return app.ErrMsg(fmt.Errorf("failed to read response body from %s: %w", sessionConfigURL, err))
		}

		objects, err := extractJSONObjects(body)
		if err != nil {
			return app.ErrMsg(fmt.Errorf("failed to extract JSON objects from response: %w", err))
		}

		// Unmarshal response into questions.Questions type
		var response questions.Questions

		for i, object := range objects {
			// Unmarshal the question
			q, err := questions.UnmarshalQuestion(object)
			if err != nil {
				return app.ErrMsg(fmt.Errorf("failed to unmarshal question at index %d: %w", i, err))
			}

			response = append(response, q)
		}

		return QuestionsGetMsg{
			Questions: response,
		}
	}
}
