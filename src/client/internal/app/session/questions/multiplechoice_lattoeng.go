package questions

import pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"

type MultipleChoiceLatToEngQuestion struct {
	*pb.MultipleChoiceLatToEngQuestion
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
