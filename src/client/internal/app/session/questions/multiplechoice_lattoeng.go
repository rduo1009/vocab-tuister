package questions

type MultipleChoiceLatToEngQuestion struct {
	Answer  string   `json:"answer"`
	Choices []string `json:"choices"`
	Prompt  string   `json:"prompt"`
}

func (q *MultipleChoiceLatToEngQuestion) QuestionMode() QuestionMode {
	return MultipleChoice
}

func (q *MultipleChoiceLatToEngQuestion) GetPrompt() string {
	return q.Prompt
}

func (q *MultipleChoiceLatToEngQuestion) GetChoices() []string {
	return q.Choices
}

func (q *MultipleChoiceLatToEngQuestion) Check(response any) bool {
	return q.Answer == response
}

func (q *MultipleChoiceLatToEngQuestion) GetMainAnswer() any {
	return q.Answer
}
