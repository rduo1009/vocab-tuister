package questions

import "github.com/rduo1009/vocab-tuister/src/client/pkg/enums"

//go:generate poetry run python3 ../../../scripts/create_question_json.py
//go:generate go run ../../../structs_generator.go

type Question interface {
	Check(response any) bool
	GetMainAnswer() any
	QuestionMode() enums.QuestionMode
	// TODO: Add view function
}

type MultipleChoiceQuestion interface {
	Question
	GetChoices() []string
}
