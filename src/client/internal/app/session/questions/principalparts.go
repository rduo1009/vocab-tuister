package questions

import (
	"slices"

	pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"
)

type PrincipalPartsQuestion struct {
	*pb.PrincipalPartsQuestion
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
