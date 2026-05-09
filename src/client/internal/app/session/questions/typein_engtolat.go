package questions

import (
	"slices"

	pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"
)

type TypeInEngToLatQuestion struct {
	*pb.TypeInEngToLatQuestion
}

func (q *TypeInEngToLatQuestion) QuestionMode() QuestionMode {
	return Regular
}

func (q *TypeInEngToLatQuestion) GetPrompt() string {
	return q.Prompt
}

func (q *TypeInEngToLatQuestion) Check(response any) bool {
	return slices.Contains(q.Answers, response.(string))
}

func (q *TypeInEngToLatQuestion) GetMainAnswer() any {
	return q.MainAnswer
}
