package questions

import (
	"github.com/google/go-cmp/cmp"
	"google.golang.org/protobuf/testing/protocmp"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions/endingcomponents"
	pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"
)

type ParseWordLatToCompQuestion struct {
	*pb.ParseWordLatToCompQuestion
}

func (q *ParseWordLatToCompQuestion) QuestionMode() QuestionMode {
	return ParseWord
}

func (q *ParseWordLatToCompQuestion) GetPrompt() string {
	return q.Prompt
}

func (q *ParseWordLatToCompQuestion) Check(response any) bool {
	responseComp := response.(endingcomponents.EndingComponents).EndingComponents

	for _, ans := range q.Answers {
		if cmp.Equal(ans, responseComp,
			protocmp.Transform(),
			protocmp.IgnoreFields(&pb.EndingComponents{}, "display_string"),
		) {
			return true
		}
	}

	return false
}

func (q *ParseWordLatToCompQuestion) GetMainAnswer() any {
	return q.MainAnswer
}
