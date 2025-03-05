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
		func(x *MultipleChoiceEngtoLatQuestion) bool {
			return x.Answer == response
		},
		func(x *MultipleChoiceLatToEngQuestion) bool {
			return x.Answer == response
		},
		func(x *ParseWordComptoLatQuestion) bool {
			responseStr := response.(string)
			return containsStr(x.Answers, responseStr)
		},
		func(x *ParseWordLattoCompQuestion) bool {
			// responseMap := response.(map[string]string)
			// return mapInSlice(x.Answers, responseMap)
			responseStr := response.(string)
			return containsStr(x.Answers, responseStr)
		},
		func(x *PrincipalPartsQuestion) bool {
			responseSlice := response.([]string)
			return slices.Equal(x.PrincipalParts, responseSlice)
		},
		func(x *TypeInEngtoLatQuestion) bool {
			responseStr := response.(string)
			return containsStr(x.Answers, responseStr)
		},
		func(x *TypeInLattoEngQuestion) bool {
			responseStr := response.(string)
			return containsStr(x.Answers, responseStr)
		},
	)
}

func GetChoices(q Question) []string {
	return MatchQuestionR1(
		q,
		func(x *MultipleChoiceEngtoLatQuestion) []string {
			return x.Choices
		},
		func(x *MultipleChoiceLatToEngQuestion) []string {
			return x.Choices
		},
		func(x *ParseWordComptoLatQuestion) []string {
			panic(fmt.Sprintf("type %T not supported by GetChoices", x))
		},
		func(x *ParseWordLattoCompQuestion) []string {
			panic(fmt.Sprintf("type %T not supported by GetChoices", x))
		},
		func(x *PrincipalPartsQuestion) []string {
			panic(fmt.Sprintf("type %T not supported by GetChoices", x))
		},
		func(x *TypeInEngtoLatQuestion) []string {
			panic(fmt.Sprintf("type %T not supported by GetChoices", x))
		},
		func(x *TypeInLattoEngQuestion) []string {
			panic(fmt.Sprintf("type %T not supported by GetChoices", x))
		},
	)
}

func GetMainAnswer(q Question) any {
	return MatchQuestionR1(
		q,
		func(x *MultipleChoiceEngtoLatQuestion) any {
			return x.Answer
		},
		func(x *MultipleChoiceLatToEngQuestion) any {
			return x.Answer
		},
		func(x *ParseWordComptoLatQuestion) any {
			return x.MainAnswer
		},
		func(x *ParseWordLattoCompQuestion) any {
			return x.MainAnswer
		},
		func(x *PrincipalPartsQuestion) any {
			return x.PrincipalParts
		},
		func(x *TypeInEngtoLatQuestion) any {
			return x.MainAnswer
		},
		func(x *TypeInLattoEngQuestion) any {
			return x.MainAnswer
		},
	)
}

func QuestionMode(q Question) enums.QuestionMode {
	return MatchQuestionR1(
		q,
		func(_ *MultipleChoiceEngtoLatQuestion) enums.QuestionMode {
			return enums.MultipleChoice
		},
		func(_ *MultipleChoiceLatToEngQuestion) enums.QuestionMode {
			return enums.MultipleChoice
		},
		func(_ *ParseWordComptoLatQuestion) enums.QuestionMode {
			return enums.Regular
		},
		func(_ *ParseWordLattoCompQuestion) enums.QuestionMode {
			return enums.Regular
		},
		func(_ *PrincipalPartsQuestion) enums.QuestionMode {
			return enums.PrincipalParts
		},
		func(_ *TypeInEngtoLatQuestion) enums.QuestionMode {
			return enums.Regular
		},
		func(_ *TypeInLattoEngQuestion) enums.QuestionMode {
			return enums.Regular
		},
	)
}
