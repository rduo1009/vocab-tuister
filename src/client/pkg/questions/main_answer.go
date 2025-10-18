package questions

func (question *MultipleChoiceEngToLatQuestion) GetMainAnswer() any {
	return question.Answer
}

func (question *MultipleChoiceLatToEngQuestion) GetMainAnswer() any {
	return question.Answer
}

func (question *ParseWordCompToLatQuestion) GetMainAnswer() any {
	return question.MainAnswer
}

func (question *ParseWordLatToCompQuestion) GetMainAnswer() any {
	return question.MainAnswer
}

func (question *PrincipalPartsQuestion) GetMainAnswer() any {
	return question.PrincipalParts
}

func (question *TypeInEngToLatQuestion) GetMainAnswer() any {
	return question.MainAnswer
}

func (question *TypeInLatToEngQuestion) GetMainAnswer() any {
	return question.MainAnswer
}
