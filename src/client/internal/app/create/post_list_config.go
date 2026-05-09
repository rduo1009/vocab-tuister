package create

import (
	"context"
	"encoding/json/v2"
	"errors"
	"fmt"
	"strings"

	tea "charm.land/bubbletea/v2"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/status"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"
)

type ErrorResponse struct {
	ErrorType string `json:"error"`
	Message   string `json:"message"`
	Details   string `json:"details,omitempty"`
}

type ListConfigPostedMsg struct {
	VocabList         string
	SessionConfig     *pb.SessionConfig
	NumberOfQuestions int
}

func postVocabList(vocabList string, client pb.VocabTesterServiceClient) (string, error) {
	if vocabList == "" {
		return "", errors.New("vocab list is empty")
	}

	_, err := client.VerifyVocab(context.Background(), &pb.VerifyVocabRequest{VocabText: vocabList})
	if err != nil {
		st, ok := status.FromError(err)
		if ok {
			switch st.Code() {
			case codes.InvalidArgument:
				return "", fmt.Errorf("invalid vocab file: %s", st.Message())

			default:
				return "", fmt.Errorf(
					"grpc error (%s): %s",
					st.Code(),
					st.Message(),
				)
			}
		}

		return "", fmt.Errorf("non-grpc error: %w", err)
	}

	return vocabList, nil
}

func postSessionConfig(rawSessionConfig string, client pb.VocabTesterServiceClient) (*pb.SessionConfig, int, error) {
	var (
		mapSessionConfig  map[string]any
		numberOfQuestions int
	)

	err := json.Unmarshal([]byte(rawSessionConfig), &mapSessionConfig)
	if err != nil {
		return nil, 0, fmt.Errorf(
			"failed to unmarshal session config: %w", err,
		)
	}

	if x, ok := mapSessionConfig["number-of-questions"]; ok {
		var y float64
		if y, ok = x.(float64); !ok {
			return nil, 0, errors.New(
				"session config does not contain number-of-questions (did not get integer)",
			)
		}

		numberOfQuestions = int(y)

		delete(mapSessionConfig, "number-of-questions")
	} else {
		return nil, 0, errors.New("session config does not contain number-of-questions")
	}

	formattedSessionConfig := make(map[string]any)
	for k, v := range mapSessionConfig {
		formattedSessionConfig[strings.ReplaceAll(k, "-", "_")] = v
	}

	formattedSessionConfigJSON, err := json.Marshal(formattedSessionConfig)
	if err != nil {
		return nil, 0, fmt.Errorf(
			"failed to marshal session config after formatting: %w",
			err,
		)
	}

	var sessionConfigStruct pb.SessionConfig
	err = json.Unmarshal(formattedSessionConfigJSON, &sessionConfigStruct)
	if err != nil {
		return nil, 0, fmt.Errorf(
			"failed to unmarshal session config after formatting: %w",
			err,
		)
	}

	_, err = client.VerifyConfig(
		context.Background(),
		&pb.VerifyConfigRequest{
			NumberOfQuestions: int32(numberOfQuestions),
			SessionConfig:     &sessionConfigStruct,
		},
	)
	if err != nil {
		st, ok := status.FromError(err)
		if ok {
			switch st.Code() {
			case codes.InvalidArgument:
				return nil, 0, fmt.Errorf("invalid session config: %s", st.Message())

			default:
				return nil, 0, fmt.Errorf(
					"grpc error (%s): %s",
					st.Code(),
					st.Message(),
				)
			}
		}

		return nil, 0, fmt.Errorf("non-grpc error: %w", err)
	}

	return &sessionConfigStruct, numberOfQuestions, nil
}

func postListConfigCmd(vocabList, rawSessionConfig string, serverPort int) tea.Cmd {
	return func() tea.Msg {
		serverURL := fmt.Sprintf(
			"localhost:%d",
			serverPort,
		)

		conn, err := grpc.NewClient(serverURL, grpc.WithTransportCredentials(insecure.NewCredentials()))
		if err != nil {
			return app.ErrMsg(fmt.Errorf(
				"failed to create grpc client for url %s: %w",
				serverURL,
				err,
			))
		}
		defer conn.Close()

		client := pb.NewVocabTesterServiceClient(conn)

		vocabList, err := postVocabList(vocabList, client)
		if err != nil {
			return app.ErrMsg(err)
		}

		sessionConfig, numberOfQuestions, err := postSessionConfig(rawSessionConfig, client)
		if err != nil {
			return app.ErrMsg(err)
		}

		return ListConfigPostedMsg{
			VocabList:         vocabList,
			SessionConfig:     sessionConfig,
			NumberOfQuestions: numberOfQuestions,
		}
	}
}
