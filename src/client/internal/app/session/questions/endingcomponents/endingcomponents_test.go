package endingcomponents_test

import (
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions/endingcomponents"
)

func TestPartOfSpeech(t *testing.T) {
	tests := []struct {
		name string
		ec   endingcomponents.EndingComponents
		want endingcomponents.PartOfSpeech
	}{
		{
			name: "Verb",
			ec: endingcomponents.EndingComponents{
				Tense:  endingcomponents.Present,
				Voice:  endingcomponents.Active,
				Mood:   endingcomponents.Indicative,
				Number: endingcomponents.Singular,
				Person: endingcomponents.FirstPerson,
			},
			want: endingcomponents.Verb,
		},
		{
			name: "Infinitive",
			ec: endingcomponents.EndingComponents{
				Tense: endingcomponents.Present,
				Voice: endingcomponents.Active,
				Mood:  endingcomponents.InfinitiveMood,
			},
			want: endingcomponents.InfinitivePOS,
		},
		{
			name: "Participle",
			ec: endingcomponents.EndingComponents{
				Tense:  endingcomponents.Perfect,
				Voice:  endingcomponents.Passive,
				Mood:   endingcomponents.ParticipleMood,
				Gender: endingcomponents.Masculine,
				Case:   endingcomponents.Nominative,
				Number: endingcomponents.Singular,
			},
			want: endingcomponents.ParticiplePOS,
		},
		{
			name: "Gerund",
			ec: endingcomponents.EndingComponents{
				Mood: endingcomponents.Gerund,
				Case: endingcomponents.Genitive,
			},
			want: endingcomponents.VerbalNoun,
		},
		{
			name: "Supine",
			ec: endingcomponents.EndingComponents{
				Mood: endingcomponents.Supine,
				Case: endingcomponents.Accusative,
			},
			want: endingcomponents.VerbalNoun,
		},
		{
			name: "Adjective",
			ec: endingcomponents.EndingComponents{
				Degree: endingcomponents.Superlative,
				Case:   endingcomponents.Nominative,
				Number: endingcomponents.Singular,
				Gender: endingcomponents.Feminine,
			},
			want: endingcomponents.Adjective,
		},
		{
			name: "Pronoun",
			ec: endingcomponents.EndingComponents{
				Case:   endingcomponents.Nominative,
				Number: endingcomponents.Singular,
				Gender: endingcomponents.Masculine,
			},
			want: endingcomponents.Pronoun,
		},
		{
			name: "Noun",
			ec: endingcomponents.EndingComponents{
				Case:   endingcomponents.Nominative,
				Number: endingcomponents.Singular,
			},
			want: endingcomponents.Noun,
		},
		{
			name: "Adverb",
			ec: endingcomponents.EndingComponents{
				Degree: endingcomponents.Comparative,
			},
			want: endingcomponents.Adverb,
		},
		{
			name: "RegularWord",
			ec:   endingcomponents.EndingComponents{},
			want: endingcomponents.RegularWord,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			assert.Equal(t, tt.want, tt.ec.PartOfSpeech())
		})
	}
}

func TestEndingComponentsString(t *testing.T) {
	// These tests assume stringer generated the expected values (nominative, singular, etc.)
	// Since we are not running go generate, we simulate the expected output
	// based on the // linecomments in the source code.
	tests := []struct {
		name string
		ec   endingcomponents.EndingComponents
		want string
	}{
		{
			name: "Verb",
			ec: endingcomponents.EndingComponents{
				Tense:  endingcomponents.Perfect,
				Voice:  endingcomponents.Active,
				Mood:   endingcomponents.Indicative,
				Number: endingcomponents.Singular,
				Person: endingcomponents.ThirdPerson,
			},
			want: "perfect active indicative singular 3rd person",
		},
		{
			name: "Infinitive",
			ec: endingcomponents.EndingComponents{
				Tense: endingcomponents.Present,
				Voice: endingcomponents.Active,
				Mood:  endingcomponents.InfinitiveMood,
			},
			want: "present active infinitive",
		},
		{
			name: "Gerundive",
			ec: endingcomponents.EndingComponents{
				Tense:  endingcomponents.Future,
				Voice:  endingcomponents.Passive,
				Mood:   endingcomponents.ParticipleMood,
				Gender: endingcomponents.Feminine,
				Case:   endingcomponents.Nominative,
				Number: endingcomponents.Singular,
			},
			want: "gerundive feminine nominative singular",
		},
		{
			name: "Participle",
			ec: endingcomponents.EndingComponents{
				Tense:  endingcomponents.Present,
				Voice:  endingcomponents.Active,
				Mood:   endingcomponents.ParticipleMood,
				Gender: endingcomponents.Neuter,
				Case:   endingcomponents.Accusative,
				Number: endingcomponents.Plural,
			},
			want: "present active participle neuter accusative plural",
		},
		{
			name: "Adverb",
			ec: endingcomponents.EndingComponents{
				Degree: endingcomponents.Comparative,
			},
			want: "comparative (adverb)",
		},
		{
			name: "Adjective",
			ec: endingcomponents.EndingComponents{
				Degree: endingcomponents.Superlative,
				Case:   endingcomponents.Nominative,
				Number: endingcomponents.Singular,
				Gender: endingcomponents.Feminine,
			},
			want: "superlative nominative singular feminine",
		},
		{
			name: "Noun",
			ec: endingcomponents.EndingComponents{
				Case:   endingcomponents.Genitive,
				Number: endingcomponents.Plural,
			},
			want: "genitive plural",
		},
		{
			name: "RegularWord",
			ec:   endingcomponents.EndingComponents{},
			want: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Note: This relies on String() methods correctly returning values.
			// Since we can't run stringer, we just check the structure.
			// In a real environment, stringer would be run first.
			got := tt.ec.String()
			assert.Equal(t, tt.want, got)
		})
	}
}
