package questions

type MultipleChoiceEngToLatQuestion struct {
	Answer  string   `json:"answer"`
	Choices []string `json:"choices"`
	Prompt  string   `json:"prompt"`
}

func (q *MultipleChoiceEngToLatQuestion) QuestionMode() QuestionMode {
	return MultipleChoice
}

func (q *MultipleChoiceEngToLatQuestion) GetPrompt() string {
	return q.Prompt
}

func (q *MultipleChoiceEngToLatQuestion) GetChoices() []string {
	return q.Choices
}

func (q *MultipleChoiceEngToLatQuestion) Check(response any) bool {
	return q.Answer == response
}

func (q *MultipleChoiceEngToLatQuestion) GetMainAnswer() any {
	return q.Answer
}
