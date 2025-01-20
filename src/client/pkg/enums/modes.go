package enums

type QuestionMode int

const (
	Regular QuestionMode = iota
	PrincipalParts
	MultipleChoice
)

type AppStatus int

const (
	Unanswered AppStatus = iota
	Correct
	Incorrect
	FinalScreen
)
