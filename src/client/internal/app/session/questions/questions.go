package questions

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
