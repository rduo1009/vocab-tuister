package questions

import (
	"slices"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions/endingcomponents"
)

type ParseWordLatToCompQuestion struct {
	Answers         []endingcomponents.EndingComponents `json:"answers"`
	DictionaryEntry string                              `json:"dictionary_entry"`
	MainAnswer      endingcomponents.EndingComponents   `json:"main_answer"`
	Prompt          string                              `json:"prompt"`
}

func (q *ParseWordLatToCompQuestion) QuestionMode() QuestionMode {
	return ParseWord
}

func (q *ParseWordLatToCompQuestion) GetPrompt() string {
	return q.Prompt
}

func (q *ParseWordLatToCompQuestion) Check(response any) bool {
	responseComp := response.(endingcomponents.EndingComponents)
	return slices.Contains(q.Answers, responseComp)
}

func (q *ParseWordLatToCompQuestion) GetMainAnswer() any {
	return q.MainAnswer
}
