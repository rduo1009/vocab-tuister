package questions

import (
	"slices"
)

// NOTE: Commented out code is code that may be required if the format of the tui changes
// func mapInSlice(a []map[string]string, b map[string]string) bool {
// 	for _, item := range a {
// 		if maps.Equal(b, item) {
// 			return true
// 		}
// 	}
// 	return false
// }

func (question *MultipleChoiceEngToLatQuestion) Check(response any) bool {
	return question.Answer == response
}

func (question *MultipleChoiceLatToEngQuestion) Check(response any) bool {
	return question.Answer == response
}

func (question *ParseWordCompToLatQuestion) Check(response any) bool {
	return slices.Contains(question.Answers, response.(string))
}

func (question *ParseWordLatToCompQuestion) Check(response any) bool {
	// responseMap := response.(map[string]string)
	// return mapInSlice(question.Answers, responseMap)
	return slices.Contains(question.Answers, response.(string))
}

func (question *PrincipalPartsQuestion) Check(response any) bool {
	return slices.Equal(question.PrincipalParts, response.([]string))
}

func (question *TypeInEngToLatQuestion) Check(response any) bool {
	return slices.Contains(question.Answers, response.(string))
}

func (question *TypeInLatToEngQuestion) Check(response any) bool {
	return slices.Contains(question.Answers, response.(string))
}
