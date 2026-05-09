package session

import (
	"context"
	"fmt"
	"io"

	tea "charm.land/bubbletea/v2"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/status"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions"
	pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"
)

type QuestionProvider interface {
	// Next returns the next question (as a [questions.Question]), handling errors.
	Next() (questions.Question, error)

	// Current returns the number of the current question (counting from 1).
	Current() int

	// Close cleans up the underlying connection. Call this when the session ends.
	Close() error
}

type StreamQuestionProvider struct {
	conn     *grpc.ClientConn
	stream   grpc.ServerStreamingClient[pb.CreateSessionResponse]
	total    int
	received int
}

func (p *StreamQuestionProvider) Next() (questions.Question, error) {
	q, err := p.stream.Recv()
	if err != nil {
		if err == io.EOF {
			return nil, fmt.Errorf(
				"stream ended unexpectedly: expected %d questions, got %d",
				p.total,
				p.received,
			)
		}

		st, ok := status.FromError(err)
		if ok {
			switch st.Code() {
			case codes.InvalidArgument:
				return nil, fmt.Errorf("invalid input: %s", st.Message())
			default:
				return nil, fmt.Errorf("grpc error (%s): %s", st.Code(), st.Message())
			}
		}

		return nil, fmt.Errorf("non-grpc error: %w", err)
	}

	p.received++
	return questions.NewQuestion(q.Question), nil
}

func (p *StreamQuestionProvider) Current() int { return p.received }

func (p *StreamQuestionProvider) Close() error {
	return p.conn.Close()
}

type QuestionStreamGetMsg struct {
	QuestionProvider QuestionProvider
}

func getQuestions(serverPort int, vocabList string, sessionConfig *pb.SessionConfig, numberOfQuestions int) tea.Cmd {
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

		client := pb.NewVocabTesterServiceClient(conn)

		stream, err := client.CreateSession(
			context.Background(),
			&pb.CreateSessionRequest{
				VocabList:         vocabList,
				SessionConfig:     sessionConfig,
				NumberOfQuestions: int32(numberOfQuestions),
			},
		)
		if err != nil {
			st, ok := status.FromError(err)
			if ok {
				switch st.Code() {
				case codes.InvalidArgument:
					return app.ErrMsg(fmt.Errorf(
						"invalid input: %s",
						st.Message(),
					))

				default:
					return app.ErrMsg(fmt.Errorf(
						"grpc error (%s): %s",
						st.Code(),
						st.Message(),
					))
				}
			}

			return app.ErrMsg(fmt.Errorf("non-grpc error: %w", err))
		}

		return QuestionStreamGetMsg{
			QuestionProvider: &StreamQuestionProvider{
				conn:   conn,
				stream: stream,
				total:  numberOfQuestions,
			},
		}
	}
}
