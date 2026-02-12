package root

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"time"

	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/types/sessionconfig"
)

type ListConfigLoadedMsg struct {
	vocabList     string
	sessionConfig sessionconfig.SessionConfig
}

func loadVocabList(vocabList string, serverPort int) (string, error) {
	if vocabList == "" {
		return "", errors.New("vocab list is empty")
	}

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	client := &http.Client{}

	vocabListURL := fmt.Sprintf(
		"http://localhost:%d/%s",
		serverPort,
		vocabListPage,
	)

	req, err := http.NewRequestWithContext(
		ctx,
		http.MethodPost,
		vocabListURL,
		bytes.NewBuffer([]byte(vocabList)),
	)
	if err != nil {
		return "", fmt.Errorf("failed to create HTTP request for vocab list to %s: %w", vocabListURL, err)
	}

	req.Header.Set("Content-Type", "text/plain")

	resp, err := client.Do(req)
	if err != nil {
		return "", fmt.Errorf("failed to post vocab list to %s: %w", vocabListURL, err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)

		var errorResponse ErrorResponse
		if err := json.Unmarshal(body, &errorResponse); err != nil {
			return "", fmt.Errorf("failed to unmarshal error response: %w", err)
		}

		return "", fmt.Errorf(
			"failed to post vocab file to %s, status code: %d, response: %s",
			vocabListURL,
			resp.StatusCode,
			errorResponse.Message,
		)
	}

	return vocabList, nil
}

func loadSessionConfig(rawSessionConfig string, serverPort int) (sessionconfig.SessionConfig, error) {
	var (
		mapSessionConfig  map[string]any
		numberOfQuestions int
	)

	err := json.Unmarshal([]byte(rawSessionConfig), &mapSessionConfig)
	if err != nil {
		return sessionconfig.SessionConfig{}, fmt.Errorf(
			"failed to unmarshal session config: %w", err,
		)
	}

	if x, ok := mapSessionConfig["number-of-questions"]; ok {
		var y float64
		if y, ok = x.(float64); !ok {
			return sessionconfig.SessionConfig{}, errors.New(
				"session config does not contain number-of-questions (did not get integer)",
			)
		}

		numberOfQuestions = int(y)

		delete(mapSessionConfig, "number-of-questions")
	} else {
		return sessionconfig.SessionConfig{}, errors.New("session config does not contain number-of-questions")
	}

	toSend := map[string]any{
		"number-of-questions": numberOfQuestions,
		"config":              mapSessionConfig,
	}

	sessionConfigData, err := json.Marshal(toSend)
	if err != nil {
		return sessionconfig.SessionConfig{}, fmt.Errorf(
			"failed to marshal session config with number-of-questions: %w",
			err,
		)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	client := &http.Client{}

	// Send session config to server
	sessionConfigURL := fmt.Sprintf(
		"http://localhost:%d/%s",
		serverPort,
		sessionConfigPage,
	)

	req, err := http.NewRequestWithContext(
		ctx,
		http.MethodPost,
		sessionConfigURL,
		bytes.NewBuffer(sessionConfigData),
	)
	if err != nil {
		return sessionconfig.SessionConfig{}, fmt.Errorf(
			"failed to create HTTP request for session config to %s: %w", sessionConfigURL, err,
		)
	}

	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)
	if err != nil {
		return sessionconfig.SessionConfig{}, fmt.Errorf(
			"failed to post session config to %s: %w", sessionConfigURL, err,
		)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)

		var errorResponse ErrorResponse
		if err := json.Unmarshal(body, &errorResponse); err != nil {
			return sessionconfig.SessionConfig{}, fmt.Errorf("failed to unmarshal error response: %w", err)
		}

		return sessionconfig.SessionConfig{}, fmt.Errorf(
			"failed to post session config to %s, status code: %d, response: %s",
			sessionConfigURL,
			resp.StatusCode,
			errorResponse.Message,
		)
	}

	// The sessionConfigData has been verified by the server now, so we can unmarshal it
	// into a sessionconfig.SessionConfig type
	var sessionConfig sessionconfig.SessionConfig

	err = json.Unmarshal([]byte(rawSessionConfig), &sessionConfig)
	if err != nil {
		return sessionconfig.SessionConfig{}, fmt.Errorf("failed to unmarshal verified session config: %w", err)
	}

	return sessionConfig, nil
}

func loadDataCmd(vocabList, rawSessionConfig string, serverPort int) tea.Cmd {
	return func() tea.Msg {
		vocabList, err := loadVocabList(vocabList, serverPort)
		if err != nil {
			return app.ErrMsg(err)
		}

		sessionConfig, err := loadSessionConfig(rawSessionConfig, serverPort)
		if err != nil {
			return app.ErrMsg(err)
		}

		return ListConfigLoadedMsg{
			vocabList:     vocabList,
			sessionConfig: sessionConfig,
		}
	}
}
