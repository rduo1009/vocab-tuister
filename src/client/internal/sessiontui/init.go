package sessiontui

import (
	"bytes"
	"context"
	"encoding/json/jsontext"
	"encoding/json/v2"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"

	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
	unionjson "github.com/widmogrod/mkunion/x/shared"

	"github.com/rduo1009/vocab-tuister/src/client/pkg"
	"github.com/rduo1009/vocab-tuister/src/client/pkg/questions"
)

const (
	vocabListPage = "send-vocab"
	sessionPage   = "session"
)

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

func (m Model) Init() tea.Cmd {
	return tea.Batch(
		textinput.Blink,
		tea.SetWindowTitle("Vocab Tester Session"),
		func() tea.Msg {
			// Read vocab and session config files
			vocabListData, err := os.ReadFile(m.vocabListPath)
			if err != nil {
				return errMsg{err}
			}

			sessionConfigPath := m.sessionConfigPath
			sessionConfigData, err := os.ReadFile(sessionConfigPath)
			if err != nil {
				return errMsg{err}
			}

			// Add user provided number of questions to temporary session config map
			var rawSessionConfig map[string]any
			err = json.Unmarshal(sessionConfigData, &rawSessionConfig)
			if err != nil {
				return errMsg{err}
			}
			rawSessionConfig["number-of-questions"] = m.numberOfQuestions

			// Marshal the updated session config
			sessionConfigData, err = json.Marshal(rawSessionConfig)
			if err != nil {
				return errMsg{err}
			}

			ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
			defer cancel()

			client := &http.Client{}

			// Send vocab file text to server
			vocabListURL := fmt.Sprintf(
				"http://localhost:%d/%s",
				m.serverPort,
				vocabListPage,
			)
			vocabList := string(vocabListData)

			req1, err := http.NewRequestWithContext(
				ctx,
				http.MethodPost,
				vocabListURL,
				bytes.NewBuffer([]byte(vocabList)),
			)
			if err != nil {
				return errMsg{err}
			}
			req1.Header.Set("Content-Type", "text/plain")

			resp1, err := client.Do(req1)
			if err != nil {
				return errMsg{err}
			}
			defer resp1.Body.Close()

			if resp1.StatusCode != http.StatusOK {
				return errMsg{
					fmt.Errorf(
						"failed to post vocab file, status code: %d",
						resp1.StatusCode,
					),
				}
			}

			// Send session config to server
			sessionConfigURL := fmt.Sprintf(
				"http://localhost:%d/%s",
				m.serverPort,
				sessionPage,
			)
			req2, err := http.NewRequestWithContext(
				ctx,
				http.MethodPost,
				sessionConfigURL,
				bytes.NewBuffer(sessionConfigData),
			)
			if err != nil {
				return errMsg{err}
			}
			req2.Header.Set("Content-Type", "application/json")

			resp2, err := client.Do(req2)
			if err != nil {
				return errMsg{err}
			}
			defer resp2.Body.Close()

			if resp2.StatusCode != http.StatusOK {
				return errMsg{
					fmt.Errorf(
						"failed to post session config, status code: %d",
						resp2.StatusCode,
					),
				}
			}

			// Read response from server
			body, err := io.ReadAll(resp2.Body)
			if err != nil {
				return errMsg{err}
			}

			objects, err := extractJSONObjects(body)
			if err != nil {
				return errMsg{err}
			}

			// Unmarshal response into questions.Questions type
			var response questions.Questions
			for _, object := range objects {
				part, err := unionjson.JSONUnmarshal[questions.Question](object)
				if err != nil {
					return errMsg{err}
				}
				response = append(response, part)
			}

			if len(response) != m.numberOfQuestions {
				return errMsg{
					fmt.Errorf(
						"expected %d questions, got %d",
						m.numberOfQuestions,
						len(response),
					),
				}
			}

			// The sessionConfigData has been verified by the server now, so we can unmarshal it
			// into a pkg.SessionConfig type
			var sessionConfig pkg.SessionConfig
			err = json.Unmarshal(sessionConfigData, &sessionConfig)
			if err != nil {
				return errMsg{err}
			}

			return initOkMsg{
				vocabList:     vocabList,
				sessionConfig: sessionConfig,
				questions:     response,
			}
		},
	)
}
