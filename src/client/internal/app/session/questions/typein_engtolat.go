package questions

import (
	"slices"
)

type TypeInEngToLatQuestion struct {
	Answers    []string `json:"answers"`
	MainAnswer string   `json:"main_answer"`
	Prompt     string   `json:"prompt"`
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
