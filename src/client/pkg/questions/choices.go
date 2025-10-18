package questions

func (question *MultipleChoiceEngToLatQuestion) GetChoices() []string {
	return question.Choices
}

func (question *MultipleChoiceLatToEngQuestion) GetChoices() []string {
	return question.Choices
}
