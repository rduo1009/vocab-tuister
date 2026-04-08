package questions

import (
	"slices"
)

type PrincipalPartsQuestion struct {
	PrincipalParts []string `json:"principal_parts"`
	Prompt         string   `json:"prompt"`
}

func (q *PrincipalPartsQuestion) QuestionMode() QuestionMode {
	return PrincipalParts
}

func (q *PrincipalPartsQuestion) GetPrompt() string {
	return q.Prompt
}

func (q *PrincipalPartsQuestion) Check(response any) bool {
	return slices.Equal(q.PrincipalParts, response.([]string))
}

func (q *PrincipalPartsQuestion) GetMainAnswer() any {
	return q.PrincipalParts
}
