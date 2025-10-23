package questions

import (
	"github.com/rduo1009/vocab-tuister/src/client/internal/types/modes"
)

func (question *MultipleChoiceEngToLatQuestion) QuestionMode() modes.QuestionMode {
	return modes.MultipleChoice
}

func (question *MultipleChoiceLatToEngQuestion) QuestionMode() modes.QuestionMode {
	return modes.MultipleChoice
}

func (question *ParseWordCompToLatQuestion) QuestionMode() modes.QuestionMode {
	return modes.Regular
}

func (question *ParseWordLatToCompQuestion) QuestionMode() modes.QuestionMode {
	return modes.Regular
}

func (question *PrincipalPartsQuestion) QuestionMode() modes.QuestionMode {
	return modes.PrincipalParts
}

func (question *TypeInEngToLatQuestion) QuestionMode() modes.QuestionMode {
	return modes.Regular
}

func (question *TypeInLatToEngQuestion) QuestionMode() modes.QuestionMode {
	return modes.Regular
}
