package questions

import (
	"slices"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions/endingcomponents"
)

type ParseWordCompToLatQuestion struct {
	Answers    []string                          `json:"answers"`
	Components endingcomponents.EndingComponents `json:"components"`
	MainAnswer string                            `json:"main_answer"`
	Prompt     string                            `json:"prompt"`
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
