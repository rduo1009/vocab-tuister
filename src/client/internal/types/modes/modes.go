package modes

// XXX: Should all of these be moved into the packages where they are used?

//go:generate go tool stringer -type=PageName -output=pagename_string_gen.go
type PageName int

const (
	Create PageName = iota
	Review
	Test
	Help
	Settings
)

type OptionType int

const (
	OptionBool OptionType = iota
	OptionText
	OptionNumber
	OptionSelect
)

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
