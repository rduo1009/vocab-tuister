package questions_test

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/rduo1009/vocab-tuister/src/client/pkg/enums"
	"github.com/rduo1009/vocab-tuister/src/client/pkg/questions"
)

func TestCheck(t *testing.T) {
	tests := map[string]struct {
		question questions.Question
		input    any
		want     bool
	}{
		"MultipleChoiceEngtoLatQuestion_1": {
			question: &questions.MultipleChoiceEngToLatQuestion{Prompt: "that", Choices: []string{"audio", "ille", "nomen"}, Answer: "ille"},
			input:    "ille", want: true,
		},
		"MultipleChoiceEngtoLatQuestion_2": {
			question: &questions.MultipleChoiceEngToLatQuestion{Prompt: "from", Choices: []string{"hic", "e", "capio"}, Answer: "e"},
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
			question: &questions.ParseWordCompToLatQuestion{Prompt: "that: ille, illa, illud", Components: "dative singular neuter", MainAnswer: "illi", Answers: []string{"illi"}},
			input:    "illi", want: true,
		},
		"ParseWordComptoLatQuestion_2": {
			question: &questions.ParseWordCompToLatQuestion{Prompt: "boy: puer, pueri, (m)", Components: "genitive singular", MainAnswer: "pueri", Answers: []string{"pueri"}},
			input:    "puer", want: false,
		},
		"ParseWordLattoCompQuestion_1": {
			question: &questions.ParseWordLatToCompQuestion{Prompt: "captae", DictionaryEntry: "take: capio, capere, cepi, captus", MainAnswer: "perfect passive participle feminine dative singular", Answers: []string{"perfect passive participle feminine dative singular"}},
			input:    "perfect passive participle feminine dative singular", want: true,
		},
		"ParseWordLattoCompQuestion_2": {
			question: &questions.ParseWordLatToCompQuestion{Prompt: "laetissimam", DictionaryEntry: "happy: laetus, laeta, laetum, (2-1-2)", MainAnswer: "superlative accusative singular feminine", Answers: []string{"superlative accusative singular feminine"}},
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
			question: &questions.TypeInEngToLatQuestion{Prompt: "into", MainAnswer: "in", Answers: []string{"in"}},
			input:    "in", want: true,
		},
		"TypeInEngtoLatQuestion_2": {
			question: &questions.TypeInEngToLatQuestion{Prompt: "from", MainAnswer: "e", Answers: []string{"e"}},
			input:    "in", want: false,
		},
		"TypeInEngtoLatQuestion_3": {
			question: &questions.TypeInEngToLatQuestion{Prompt: "large", MainAnswer: "ingens", Answers: []string{"ingens", "ingentem", "ingentes", "ingenti", "ingentia", "ingentibus", "ingentis", "ingentium"}},
			input:    "ingentibus", want: true,
		},
		"TypeInEngtoLatQuestion_4": {
			question: &questions.TypeInLatToEngQuestion{Prompt: "very happy", MainAnswer: "laetissimus", Answers: []string{"laetissima", "laetissimae", "laetissimam", "laetissimarum", "laetissimas", "laetissime", "laetissimi", "laetissimis", "laetissimo", "laetissimorum", "laetissimos", "laetissimum", "laetissimus"}},
			input:    "laetus", want: false,
		},
		"TypeInLattoEngQuestion_1": {
			question: &questions.TypeInLatToEngQuestion{Prompt: "ingenti", MainAnswer: "large", Answers: []string{"large"}},
			input:    "large", want: true,
		},
		"TypeInLattoEngQuestion_2": {
			question: &questions.TypeInLatToEngQuestion{Prompt: "capente", MainAnswer: "taking", Answers: []string{"taking"}},
			input:    "I am taking", want: false,
		},
		"TypeInLattoEngQuestion_3": {
			question: &questions.TypeInLatToEngQuestion{Prompt: "puero", MainAnswer: "by the boy", Answers: []string{"boy", "by a boy", "by means of a boy", "by means of the boy", "by the boy", "for a boy", "for the boy", "to a boy", "to the boy", "with a boy", "with the boy"}},
			input:    "for the boy", want: true,
		},
		"TypeInLattoEngQuestion_4": {
			question: &questions.TypeInLatToEngQuestion{Prompt: "illa", MainAnswer: "those", Answers: []string{"by means of that", "by that", "that", "those", "with that"}},
			input:    "by means of those", want: false,
		},
	}

	for name, tt := range tests {
		t.Run(name, func(t *testing.T) {
			got := questions.Check(tt.question, tt.input)
			assert.Equal(t, tt.want, got, fmt.Sprintf("expected %t, got %t (test %s)", tt.want, got, name))
		})
	}
}

func TestGetChoices(t *testing.T) {
	tests := map[string]struct {
		question questions.Question
		want     []string
		wantErr  error
	}{
		"MultipleChoiceEngToLatQuestion": {
			question: &questions.MultipleChoiceEngToLatQuestion{Prompt: "that", Choices: []string{"audio", "ille", "nomen"}, Answer: "ille"},
			want:     []string{"audio", "ille", "nomen"},
			wantErr:  nil,
		},
		"MultipleChoiceLatToEngQuestion": {
			question: &questions.MultipleChoiceLatToEngQuestion{Prompt: "puer", Choices: []string{"name", "boy", "hear"}, Answer: "boy"},
			want:     []string{"name", "boy", "hear"},
			wantErr:  nil,
		},
		"ParseWordCompToLatQuestion": {
			question: &questions.ParseWordCompToLatQuestion{Prompt: "that: ille, illa, illud", Components: "dative singular neuter", MainAnswer: "illi", Answers: []string{"illi"}},
			want:     []string(nil),
			wantErr:  fmt.Errorf("type *questions.ParseWordCompToLatQuestion not supported by GetChoices"),
		},
		"ParseWordLatToCompQuestion": {
			question: &questions.ParseWordLatToCompQuestion{Prompt: "captae", DictionaryEntry: "take: capio, capere, cepi, captus", MainAnswer: "perfect passive participle feminine dative singular", Answers: []string{"perfect passive participle feminine dative singular"}},
			want:     []string(nil),
			wantErr:  fmt.Errorf("type *questions.ParseWordLatToCompQuestion not supported by GetChoices"),
		},
		"PrincipalPartsQuestion": {
			question: &questions.PrincipalPartsQuestion{Prompt: "ingens", PrincipalParts: []string{"ingens", "ingentis"}},
			want:     []string(nil),
			wantErr:  fmt.Errorf("type *questions.PrincipalPartsQuestion not supported by GetChoices"),
		},
		"TypeInEngToLatQuestion": {
			question: &questions.TypeInEngToLatQuestion{Prompt: "into", MainAnswer: "in", Answers: []string{"in"}},
			want:     []string(nil),
			wantErr:  fmt.Errorf("type *questions.TypeInEngToLatQuestion not supported by GetChoices"),
		},
		"TypeInLatToEngQuestion": {
			question: &questions.TypeInLatToEngQuestion{Prompt: "ingenti", MainAnswer: "large", Answers: []string{"large"}},
			want:     []string(nil),
			wantErr:  fmt.Errorf("type *questions.TypeInLatToEngQuestion not supported by GetChoices"),
		},
	}

	for name, tt := range tests {
		t.Run(name, func(t *testing.T) {
			var gotErr error
			var got []string

			defer func() {
				if r := recover(); r != nil {
					if err, ok := r.(error); ok {
						gotErr = err
					} else {
						gotErr = fmt.Errorf("%v", r)
					}
				}

				assert.Equal(t, tt.wantErr, gotErr, fmt.Sprintf("expected %t, got %t (test %s)", tt.wantErr, gotErr, name))
				assert.Equal(t, tt.want, got, fmt.Sprintf("expected %v, got %v (test %s)", tt.want, got, name))
			}()

			got = questions.GetChoices(tt.question)
		})
	}
}

func TestMainAnswer(t *testing.T) {
	tests := map[string]struct {
		question questions.Question
		want     any
	}{
		"MultipleChoiceEngToLatQuestion": {
			question: &questions.MultipleChoiceEngToLatQuestion{Prompt: "that", Choices: []string{"audio", "ille", "nomen"}, Answer: "ille"},
			want:     "ille",
		},
		"MultipleChoiceLatToEngQuestion": {
			question: &questions.MultipleChoiceLatToEngQuestion{Prompt: "puer", Choices: []string{"name", "boy", "hear"}, Answer: "boy"},
			want:     "boy",
		},
		"ParseWordCompToLatQuestion": {
			question: &questions.ParseWordCompToLatQuestion{Prompt: "that: ille, illa, illud", Components: "dative singular neuter", MainAnswer: "illi", Answers: []string{"illi"}},
			want:     "illi",
		},
		"ParseWordLatToCompQuestion": {
			question: &questions.ParseWordLatToCompQuestion{Prompt: "captae", DictionaryEntry: "take: capio, capere, cepi, captus", MainAnswer: "perfect passive participle feminine dative singular", Answers: []string{"perfect passive participle feminine dative singular"}},
			want:     "perfect passive participle feminine dative singular",
		},
		"PrincipalPartsQuestion": {
			question: &questions.PrincipalPartsQuestion{Prompt: "ingens", PrincipalParts: []string{"ingens", "ingentis"}},
			want:     []string{"ingens", "ingentis"},
		},
		"TypeInEngToLatQuestion": {
			question: &questions.TypeInEngToLatQuestion{Prompt: "into", MainAnswer: "in", Answers: []string{"in"}},
			want:     "in",
		},
		"TypeInLatToEngQuestion": {
			question: &questions.TypeInLatToEngQuestion{Prompt: "ingenti", MainAnswer: "large", Answers: []string{"large"}},
			want:     "large",
		},
	}

	for name, tt := range tests {
		t.Run(name, func(t *testing.T) {
			got := questions.GetMainAnswer(tt.question)
			assert.Equal(t, tt.want, got, fmt.Sprintf("expected %t, got %t (test %s)", tt.want, got, name))
		})
	}
}

func TestQuestionMode(t *testing.T) {
	tests := map[string]struct {
		question questions.Question
		want     enums.QuestionMode
	}{
		"MultipleChoiceEngToLatQuestion": {
			question: &questions.MultipleChoiceEngToLatQuestion{Prompt: "that", Choices: []string{"audio", "ille", "nomen"}, Answer: "ille"},
			want:     enums.MultipleChoice,
		},
		"MultipleChoiceLatToEngQuestion": {
			question: &questions.MultipleChoiceLatToEngQuestion{Prompt: "puer", Choices: []string{"name", "boy", "hear"}, Answer: "boy"},
			want:     enums.MultipleChoice,
		},
		"ParseWordCompToLatQuestion": {
			question: &questions.ParseWordCompToLatQuestion{Prompt: "that: ille, illa, illud", Components: "dative singular neuter", MainAnswer: "illi", Answers: []string{"illi"}},
			want:     enums.Regular,
		},
		"ParseWordLatToCompQuestion": {
			question: &questions.ParseWordLatToCompQuestion{Prompt: "captae", DictionaryEntry: "take: capio, capere, cepi, captus", MainAnswer: "perfect passive participle feminine dative singular", Answers: []string{"perfect passive participle feminine dative singular"}},
			want:     enums.Regular,
		},
		"PrincipalPartsQuestion": {
			question: &questions.PrincipalPartsQuestion{Prompt: "ingens", PrincipalParts: []string{"ingens", "ingentis"}},
			want:     enums.PrincipalParts,
		},
		"TypeInEngToLatQuestion": {
			question: &questions.TypeInEngToLatQuestion{Prompt: "into", MainAnswer: "in", Answers: []string{"in"}},
			want:     enums.Regular,
		},
		"TypeInLatToEngQuestion": {
			question: &questions.TypeInLatToEngQuestion{Prompt: "ingenti", MainAnswer: "large", Answers: []string{"large"}},
			want:     enums.Regular,
		},
	}

	for name, tt := range tests {
		t.Run(name, func(t *testing.T) {
			got := questions.QuestionMode(tt.question)
			assert.Equal(t, tt.want, got, fmt.Sprintf("expected %v, got %v (test %s)", tt.want, got, name))
		})
	}
}
