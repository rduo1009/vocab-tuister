package sessiontui

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"

	"github.com/charmbracelet/bubbles/v2/textinput"
	tea "github.com/charmbracelet/bubbletea/v2"
	unionjson "github.com/widmogrod/mkunion/x/shared"

	"github.com/rduo1009/vocab-tuister/src/client/pkg"
	"github.com/rduo1009/vocab-tuister/src/client/pkg/questions"
)

const (
	vocabListPage = "send-vocab"
	sessionPage   = "session"
)

func extractJSONObjects(jsonList []byte) ([][]byte, error) {
	var rawSlice []json.RawMessage
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

func (m model) Init() (tea.Model, tea.Cmd) {
	return m, tea.Batch(textinput.Blink, tea.SetWindowTitle("Vocab Tester Session"), func() tea.Msg {
		vocabListData, err := os.ReadFile(m.vocabListPath)
		if err != nil {
			return errMsg{err}
		}

		sessionConfigPath := m.sessionConfigPath
		sessionConfigData, err := os.ReadFile(sessionConfigPath)
		if err != nil {
			return errMsg{err}
		}

		var sessionConfig pkg.SessionConfig
		err = json.Unmarshal(sessionConfigData, &sessionConfig)
		if err != nil {
			return errMsg{err}
		}
		sessionConfig.NumberOfQuestions = m.numberOfQuestions

		sessionConfigData, err = json.Marshal(sessionConfig)
		if err != nil {
			return errMsg{err}
		}

		ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
		defer cancel()

		client := &http.Client{}

		vocabListURL := fmt.Sprintf("http://localhost:%d/%s", m.serverPort, vocabListPage)
		vocabList := string(vocabListData)

		req1, err := http.NewRequestWithContext(ctx, http.MethodPost, vocabListURL, bytes.NewBuffer([]byte(vocabList)))
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
			return errMsg{fmt.Errorf("failed to post vocab list, status code: %d", resp1.StatusCode)}
		}

		sessionConfigURL := fmt.Sprintf("http://localhost:%d/%s", m.serverPort, sessionPage)
		req2, err := http.NewRequestWithContext(ctx, http.MethodPost, sessionConfigURL, bytes.NewBuffer(sessionConfigData))
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
			return errMsg{fmt.Errorf("failed to post session config, status code: %d", resp2.StatusCode)}
		}

		body, err := io.ReadAll(resp2.Body)
		if err != nil {
			return errMsg{err}
		}

		// NOTE: May not be the best solution but seems to work
		questionsCh := make(chan questions.Questions, 1)
		errorCh := make(chan error, 1)

		go func() {
			ticker := time.NewTicker(5 * time.Millisecond) // Poll every 500ms
			defer ticker.Stop()

			for {
				select {
				case <-ctx.Done():
					errorCh <- ctx.Err()
					return
				case <-ticker.C:
					objects, err := extractJSONObjects(body)
					if err != nil {
						errorCh <- err
						return
					}

					var response questions.Questions
					for _, object := range objects {
						part, err := unionjson.JSONUnmarshal[questions.Question](object)
						if err != nil {
							errorCh <- err
							return
						}
						response = append(response, part)
					}

					if len(response) == m.numberOfQuestions {
						questionsCh <- response
						return
					}

					req3, err := http.NewRequestWithContext(ctx, http.MethodPost, sessionConfigURL, bytes.NewBuffer(sessionConfigData))
					if err != nil {
						errorCh <- err
						return
					}
					req3.Header.Set("Content-Type", "application/json")

					resp3, err := client.Do(req3)
					if err != nil {
						errorCh <- err
						return
					}
					defer resp3.Body.Close()

					body, err = io.ReadAll(resp3.Body)
					if err != nil {
						errorCh <- err
						return
					}
				}
			}
		}()

		select {
		case questions := <-questionsCh:
			return initOkMsg{
				vocabList:     vocabList,
				sessionConfig: sessionConfig,
				questions:     questions,
			}
		case err := <-errorCh:
			return errMsg{fmt.Errorf("failed to get all questions: %w", err)}
		}
	})
}
