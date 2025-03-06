package questions

import (
	"fmt"
	"slices"

	"github.com/rduo1009/vocab-tuister/src/client/pkg/enums"
)

var containsStr = slices.Contains[[]string, string]

// NOTE: Commented out code is code that may be required if the format of the tui changes
// func mapInSlice(a []map[string]string, b map[string]string) bool {
// 	for _, item := range a {
// 		if maps.Equal(b, item) {
// 			return true
// 		}
// 	}
// 	return false
// }

func Check(q Question, response any) bool {
	return MatchQuestionR1(
		q,
		func(x *MultipleChoiceEngToLatQuestion) bool {
			return x.Answer == response
		},
		func(x *MultipleChoiceLatToEngQuestion) bool {
			return x.Answer == response
		},
		func(x *ParseWordCompToLatQuestion) bool {
			responseStr := response.(string)
			return containsStr(x.Answers, responseStr)
		},
		func(x *ParseWordLatToCompQuestion) bool {
			// responseMap := response.(map[string]string)
			// return mapInSlice(x.Answers, responseMap)
			responseStr := response.(string)
			return containsStr(x.Answers, responseStr)
		},
		func(x *PrincipalPartsQuestion) bool {
			responseSlice := response.([]string)
			return slices.Equal(x.PrincipalParts, responseSlice)
		},
		func(x *TypeInEngToLatQuestion) bool {
			responseStr := response.(string)
			return containsStr(x.Answers, responseStr)
		},
		func(x *TypeInLatToEngQuestion) bool {
			responseStr := response.(string)
			return containsStr(x.Answers, responseStr)
		},
	)
}

func GetChoices(q Question) []string {
	return MatchQuestionR1(
		q,
		func(x *MultipleChoiceEngToLatQuestion) []string {
			return x.Choices
		},
		func(x *MultipleChoiceLatToEngQuestion) []string {
			return x.Choices
		},
		func(x *ParseWordCompToLatQuestion) []string {
			panic(fmt.Sprintf("type %T not supported by GetChoices", x))
		},
		func(x *ParseWordLatToCompQuestion) []string {
			panic(fmt.Sprintf("type %T not supported by GetChoices", x))
		},
		func(x *PrincipalPartsQuestion) []string {
			panic(fmt.Sprintf("type %T not supported by GetChoices", x))
		},
		func(x *TypeInEngToLatQuestion) []string {
			panic(fmt.Sprintf("type %T not supported by GetChoices", x))
		},
		func(x *TypeInLatToEngQuestion) []string {
			panic(fmt.Sprintf("type %T not supported by GetChoices", x))
		},
	)
}

func GetMainAnswer(q Question) any {
	return MatchQuestionR1(
		q,
		func(x *MultipleChoiceEngToLatQuestion) any {
			return x.Answer
		},
		func(x *MultipleChoiceLatToEngQuestion) any {
			return x.Answer
		},
		func(x *ParseWordCompToLatQuestion) any {
			return x.MainAnswer
		},
		func(x *ParseWordLatToCompQuestion) any {
			return x.MainAnswer
		},
		func(x *PrincipalPartsQuestion) any {
			return x.PrincipalParts
		},
		func(x *TypeInEngToLatQuestion) any {
			return x.MainAnswer
		},
		func(x *TypeInLatToEngQuestion) any {
			return x.MainAnswer
		},
	)
}

func QuestionMode(q Question) enums.QuestionMode {
	return MatchQuestionR1(
		q,
		func(_ *MultipleChoiceEngToLatQuestion) enums.QuestionMode {
			return enums.MultipleChoice
		},
		func(_ *MultipleChoiceLatToEngQuestion) enums.QuestionMode {
			return enums.MultipleChoice
		},
		func(_ *ParseWordCompToLatQuestion) enums.QuestionMode {
			return enums.Regular
		},
		func(_ *ParseWordLatToCompQuestion) enums.QuestionMode {
			return enums.Regular
		},
		func(_ *PrincipalPartsQuestion) enums.QuestionMode {
			return enums.PrincipalParts
		},
		func(_ *TypeInEngToLatQuestion) enums.QuestionMode {
			return enums.Regular
		},
		func(_ *TypeInLatToEngQuestion) enums.QuestionMode {
			return enums.Regular
		},
	)
}
