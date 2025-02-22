package questions_test

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/rduo1009/vocab-tuister/src/client/pkg/questions"
)

func TestCheck(t *testing.T) {
	tests := map[string]struct {
		question questions.Question
		input    any
		want     bool
	}{
		"MultipleChoiceEngtoLatQuestion_1": {
			question: &questions.MultipleChoiceEngtoLatQuestion{Prompt: "that", Choices: []string{"audio", "ille", "nomen"}, Answer: "ille"},
			input:    "ille", want: true,
		},
		"MultipleChoiceEngtoLatQuestion_2": {
			question: &questions.MultipleChoiceEngtoLatQuestion{Prompt: "from", Choices: []string{"hic", "e", "capio"}, Answer: "e"},
			input:    "hic", want: false,
		},
		"MultipleChoiceLattoEngQuestion_1": {
			question: &questions.MultipleChoiceLatToEngQuestion{Prompt: "puer", Choices: []string{"name", "boy", "hear"}, Answer: "boy"},
			input:    "boy", want: true,
		},
		"MultipleChoiceLattoEngQuestion_2": {
			question: &questions.MultipleChoiceLatToEngQuestion{Prompt: "capio", Choices: []string{"boy", "happy", "take"}, Answer: "take"},
			input:    "boy", want: false,
		},
		"ParseWordComptoLatQuestion_1": {
			question: &questions.ParseWordComptoLatQuestion{Prompt: "that: ille, illa, illud", Components: "dative singular neuter", MainAnswer: "illi", Answers: []string{"illi"}},
			input:    "illi", want: true,
		},
		"ParseWordComptoLatQuestion_2": {
			question: &questions.ParseWordComptoLatQuestion{Prompt: "boy: puer, pueri, (m)", Components: "genitive singular", MainAnswer: "pueri", Answers: []string{"pueri"}},
			input:    "puer", want: false,
		},
		"ParseWordLattoCompQuestion_1": {
			question: &questions.ParseWordLattoCompQuestion{Prompt: "captae", DictionaryEntry: "take: capio, capere, cepi, captus", MainAnswer: "perfect passive participle feminine dative singular", Answers: []string{"perfect passive participle feminine dative singular"}},
			input:    "perfect passive participle feminine dative singular", want: true,
		},
		"ParseWordLattoCompQuestion_2": {
			question: &questions.ParseWordLattoCompQuestion{Prompt: "laetissimam", DictionaryEntry: "happy: laetus, laeta, laetum, (2-1-2)", MainAnswer: "superlative accusative singular feminine", Answers: []string{"superlative accusative singular feminine"}},
			input:    "superlative accusative singular masculine", want: false,
		},
		"PrincipalPartsQuestion_1": {
			question: &questions.PrincipalPartsQuestion{Prompt: "ingens", PrincipalParts: []string{"ingens", "ingentis"}},
			input:    []string{"ingens", "ingentis"}, want: true,
		},
		"PrincipalPartsQuestion_2": {
			question: &questions.PrincipalPartsQuestion{Prompt: "nomen", PrincipalParts: []string{"nomen", "nominis"}},
			input:    []string{"nomen", "nomini"}, want: false,
		},
		"TypeInEngtoLatQuestion_1": {
			question: &questions.TypeInEngtoLatQuestion{Prompt: "into", MainAnswer: "in", Answers: []string{"in"}},
			input:    "in", want: true,
		},
		"TypeInEngtoLatQuestion_2": {
			question: &questions.TypeInEngtoLatQuestion{Prompt: "from", MainAnswer: "e", Answers: []string{"e"}},
			input:    "in", want: false,
		},
		"TypeInEngtoLatQuestion_3": {
			question: &questions.TypeInEngtoLatQuestion{Prompt: "large", MainAnswer: "ingens", Answers: []string{"ingens", "ingentem", "ingentes", "ingenti", "ingentia", "ingentibus", "ingentis", "ingentium"}},
			input:    "ingentibus", want: true,
		},
		"TypeInEngtoLatQuestion_4": {
			question: &questions.TypeInLattoEngQuestion{Prompt: "very happy", MainAnswer: "laetissimus", Answers: []string{"laetissima", "laetissimae", "laetissimam", "laetissimarum", "laetissimas", "laetissime", "laetissimi", "laetissimis", "laetissimo", "laetissimorum", "laetissimos", "laetissimum", "laetissimus"}},
			input:    "laetus", want: false,
		},
		"TypeInLattoEngQuestion_1": {
			question: &questions.TypeInLattoEngQuestion{Prompt: "ingenti", MainAnswer: "large", Answers: []string{"large"}},
			input:    "large", want: true,
		},
		"TypeInLattoEngQuestion_2": {
			question: &questions.TypeInLattoEngQuestion{Prompt: "capente", MainAnswer: "taking", Answers: []string{"taking"}},
			input:    "I am taking", want: false,
		},
		"TypeInLattoEngQuestion_3": {
			question: &questions.TypeInLattoEngQuestion{Prompt: "puero", MainAnswer: "by the boy", Answers: []string{"boy", "by a boy", "by means of a boy", "by means of the boy", "by the boy", "for a boy", "for the boy", "to a boy", "to the boy", "with a boy", "with the boy"}},
			input:    "for the boy", want: true,
		},
		"TypeInLattoEngQuestion_4": {
			question: &questions.TypeInLattoEngQuestion{Prompt: "illa", MainAnswer: "those", Answers: []string{"by means of that", "by that", "that", "those", "with that"}},
			input:    "by means of those", want: false,
		},
	}

	for name, tt := range tests {
		t.Run(name, func(t *testing.T) {
			result := questions.Check(tt.question, tt.input)
			assert.Equal(t, tt.want, result, fmt.Sprintf("expected %t, got %t (test %s)", tt.want, result, name))
		})
	}
}
