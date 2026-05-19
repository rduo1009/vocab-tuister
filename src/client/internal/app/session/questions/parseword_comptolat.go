package questions

import (
	"slices"

	pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"
)

type ParseWordCompToLatQuestion struct {
	*pb.ParseWordCompToLatQuestion
}

func (q *ParseWordCompToLatQuestion) QuestionMode() QuestionMode {
	return Regular
}

func (q *ParseWordCompToLatQuestion) GetPrompt() string {
	return q.Prompt
}

func (q *ParseWordCompToLatQuestion) Check(response any) bool {
	return slices.Contains(q.Answers, response.(string))
}

func (q *ParseWordCompToLatQuestion) GetMainAnswer() any {
	return q.MainAnswer
}
