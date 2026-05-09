package questions

import (
	"slices"

	pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"
)

type TypeInLatToEngQuestion struct {
	*pb.TypeInLatToEngQuestion
}

func (q *TypeInLatToEngQuestion) QuestionMode() QuestionMode {
	return Regular
}

func (q *TypeInLatToEngQuestion) GetPrompt() string {
	return q.Prompt
}

func (q *TypeInLatToEngQuestion) Check(response any) bool {
	return slices.Contains(q.Answers, response.(string))
}

func (q *TypeInLatToEngQuestion) GetMainAnswer() any {
	return q.MainAnswer
}
