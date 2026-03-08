package questions

import (
	"slices"
)

type TypeInLatToEngQuestion struct {
	Answers    []string `json:"answers"`
	MainAnswer string   `json:"main_answer"`
	Prompt     string   `json:"prompt"`
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
