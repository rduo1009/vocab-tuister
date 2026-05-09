package questions

import pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"

type QuestionMode int

const (
	Regular QuestionMode = iota
	PrincipalParts
	MultipleChoice
	ParseWord
)

type (
	Questions []Question
	Question  interface {
		// QuestionMode returns the mode of the question
		QuestionMode() QuestionMode

		// GetPrompt returns the prompt for the question
		GetPrompt() string

		// Check reports whether the response is correct
		Check(response any) bool

		// GetMainAnswer returns the main answer to be displayed when the user gets an answer incorrect
		GetMainAnswer() any
	}
	MultipleChoiceQuestion interface {
		Question

		// GetChoices returns the choices for the multiple choice question
		GetChoices() []string
	}
)

func NewQuestion(q *pb.Question) Question {
	if v := q.GetMcEngToLat(); v != nil {
		return &MultipleChoiceEngToLatQuestion{v}
	}

	if v := q.GetMcLatToEng(); v != nil {
		return &MultipleChoiceLatToEngQuestion{v}
	}

	if v := q.GetParseCompToLat(); v != nil {
		return &ParseWordCompToLatQuestion{v}
	}

	if v := q.GetParseLatToComp(); v != nil {
		return &ParseWordLatToCompQuestion{v}
	}

	if v := q.GetPrincipalParts(); v != nil {
		return &PrincipalPartsQuestion{v}
	}

	if v := q.GetTypeInEngToLat(); v != nil {
		return &TypeInEngToLatQuestion{v}
	}

	if v := q.GetTypeInLatToEng(); v != nil {
		return &TypeInLatToEngQuestion{v}
	}

	return nil
}
