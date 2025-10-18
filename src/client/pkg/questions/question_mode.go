package questions

import "github.com/rduo1009/vocab-tuister/src/client/pkg/enums"

func (question *MultipleChoiceEngToLatQuestion) QuestionMode() enums.QuestionMode {
	return enums.MultipleChoice
}

func (question *MultipleChoiceLatToEngQuestion) QuestionMode() enums.QuestionMode {
	return enums.MultipleChoice
}

func (question *ParseWordCompToLatQuestion) QuestionMode() enums.QuestionMode {
	return enums.Regular
}

func (question *ParseWordLatToCompQuestion) QuestionMode() enums.QuestionMode {
	return enums.Regular
}

func (question *PrincipalPartsQuestion) QuestionMode() enums.QuestionMode {
	return enums.PrincipalParts
}

func (question *TypeInEngToLatQuestion) QuestionMode() enums.QuestionMode {
	return enums.Regular
}

func (question *TypeInLatToEngQuestion) QuestionMode() enums.QuestionMode {
	return enums.Regular
}
