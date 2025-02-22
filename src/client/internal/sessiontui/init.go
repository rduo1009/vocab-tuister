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

func (m Model) Init() (tea.Model, tea.Cmd) {
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

		objects, err := extractJSONObjects(body)
		if err != nil {
			return errMsg{err}
		}

		var response questions.Questions
		for _, object := range objects {
			part, err := unionjson.JSONUnmarshal[questions.Question](object)
			if err != nil {
				return errMsg{err}
			}
			response = append(response, part)
		}

		if len(response) != m.numberOfQuestions {
			return errMsg{fmt.Errorf("expected %d questions, got %d", m.numberOfQuestions, len(response))}
		}

		return initOkMsg{
			vocabList:     vocabList,
			sessionConfig: sessionConfig,
			questions:     response,
		}
	})
}
