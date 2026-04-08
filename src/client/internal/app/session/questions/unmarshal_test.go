package questions_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions/endingcomponents"
)

func TestUnmarshalEndingComponents(t *testing.T) {
	tests := []struct {
		input string
		want  endingcomponents.EndingComponents
	}{
		{
			input: "nominative singular masculine",
			want: endingcomponents.EndingComponents{
				Case:   endingcomponents.Nominative,
				Number: endingcomponents.Singular,
				Gender: endingcomponents.Masculine,
			},
		},
		{
			input: "perfect active indicative singular 3rd person",
			want: endingcomponents.EndingComponents{
				Tense:  endingcomponents.Perfect,
				Voice:  endingcomponents.Active,
				Mood:   endingcomponents.Indicative,
				Number: endingcomponents.Singular,
				Person: endingcomponents.ThirdPerson,
			},
		},
		{
			input: "superlative",
			want: endingcomponents.EndingComponents{
				Degree: endingcomponents.Superlative,
			},
		},
		{
			input: "imperfect passive subjunctive plural 1st person",
			want: endingcomponents.EndingComponents{
				Tense:  endingcomponents.Imperfect,
				Voice:  endingcomponents.Passive,
				Mood:   endingcomponents.Subjunctive,
				Number: endingcomponents.Plural,
				Person: endingcomponents.FirstPerson,
			},
		},
		{
			input: "future perfect infinitive",
			want: endingcomponents.EndingComponents{
				Tense: endingcomponents.FuturePerfect,
				Voice: endingcomponents.UnknownVoice, // Voice usually active/passive but test strings might vary
				Mood:  endingcomponents.InfinitiveMood,
			},
		},
		{
			input: "",
			want:  endingcomponents.EndingComponents{},
		},
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			got := questions.UnmarshalEndingComponents(tt.input)
			assert.Equal(t, tt.want, got)
		})
	}
}

func TestUnmarshalQuestion(t *testing.T) {
	tests := []struct {
		name    string
		json    string
		check   func(*testing.T, questions.Question)
		wantErr bool
	}{
		{
			name: "ParseWordCompToLatQuestion",
			json: `{"question_type": "ParseWordCompToLatQuestion", "answers": ["nomen"], "components": "nominative singular", "main_answer": "nomen", "prompt": "name: nomen, nominis, (n)"}`,
			check: func(t *testing.T, q questions.Question) {
				p, ok := q.(*questions.ParseWordCompToLatQuestion)
				require.True(t, ok)
				assert.Equal(t, "name: nomen, nominis, (n)", p.Prompt)
				assert.Equal(t, endingcomponents.Nominative, p.Components.Case)
				assert.Equal(t, endingcomponents.Singular, p.Components.Number)
			},
		},
		{
			name: "ParseWordLatToCompQuestion",
			json: `{"question_type": "ParseWordLatToCompQuestion", "answers": [{"tense": "perfect", "voice": "active", "mood": "indicative", "number": "singular", "person": "3rd person"}], "dictionary_entry": "take: capio, capere, cepi", "main_answer": {"tense": "perfect", "voice": "active", "mood": "indicative", "number": "singular", "person": "3rd person"}, "prompt": "cepit"}`,

			check: func(t *testing.T, q questions.Question) {
				p, ok := q.(*questions.ParseWordLatToCompQuestion)
				require.True(t, ok)
				assert.Equal(t, "cepit", p.Prompt)
				assert.Equal(t, endingcomponents.Perfect, p.MainAnswer.Tense)
				assert.Equal(t, endingcomponents.ThirdPerson, p.MainAnswer.Person)
				require.Len(t, p.Answers, 1)
				assert.Equal(t, endingcomponents.Perfect, p.Answers[0].Tense)
			},
		},
		{
			name: "MultipleChoiceEngToLatQuestion",
			json: `{"question_type": "MultipleChoiceEngToLatQuestion", "answer": "hic", "choices": ["agricola", "puella", "hic"], "prompt": "this"}`,
			check: func(t *testing.T, q questions.Question) {
				_, ok := q.(*questions.MultipleChoiceEngToLatQuestion)
				assert.True(t, ok)
			},
		},
		{
			name:    "UnknownType",
			json:    `{"question_type": "MagicQuestion"}`,
			wantErr: true,
		},
		{
			name:    "InvalidJSON",
			json:    `{invalid`,
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			q, err := questions.UnmarshalQuestion([]byte(tt.json))
			if tt.wantErr {
				assert.Error(t, err)
				return
			}

			require.NoError(t, err)
			tt.check(t, q)
		})
	}
}
