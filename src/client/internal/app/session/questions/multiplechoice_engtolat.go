package questions

import pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"

type MultipleChoiceEngToLatQuestion struct {
	*pb.MultipleChoiceEngToLatQuestion
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
