package endingcomponents_test

import (
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions/endingcomponents"
	pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"
)

func TestPartOfSpeech(t *testing.T) {
	tests := []struct {
		name string
		ec   endingcomponents.EndingComponents
		want endingcomponents.PartOfSpeech
	}{
		{
			name: "Verb",
			ec: endingcomponents.EndingComponents{&pb.EndingComponents{
				Tense:  pb.Tense_TENSE_PRESENT,
				Voice:  pb.Voice_VOICE_ACTIVE,
				Mood:   pb.Mood_MOOD_INDICATIVE,
				Number: pb.Number_NUMBER_SINGULAR,
				Person: pb.Person_PERSON_FIRST,
			}},
			want: endingcomponents.Verb,
		},
		{
			name: "Infinitive",
			ec: endingcomponents.EndingComponents{&pb.EndingComponents{
				Tense: pb.Tense_TENSE_PRESENT,
				Voice: pb.Voice_VOICE_ACTIVE,
				Mood:  pb.Mood_MOOD_INFINITIVE,
			}},
			want: endingcomponents.InfinitivePOS,
		},
		{
			name: "Participle",
			ec: endingcomponents.EndingComponents{&pb.EndingComponents{
				Tense:  pb.Tense_TENSE_FUTURE_PERFECT,
				Voice:  pb.Voice_VOICE_PASSIVE,
				Mood:   pb.Mood_MOOD_PARTICIPLE,
				Gender: pb.Gender_GENDER_MASCULINE,
				Case:   pb.Case_CASE_NOMINATIVE,
				Number: pb.Number_NUMBER_SINGULAR,
			}},
			want: endingcomponents.ParticiplePOS,
		},
		{
			name: "Gerund",
			ec: endingcomponents.EndingComponents{&pb.EndingComponents{
				Mood: pb.Mood_MOOD_GERUND,
				Case: pb.Case_CASE_GENITIVE,
			}},
			want: endingcomponents.VerbalNoun,
		},
		{
			name: "Supine",
			ec: endingcomponents.EndingComponents{&pb.EndingComponents{
				Mood: pb.Mood_MOOD_SUPINE,
				Case: pb.Case_CASE_ACCUSATIVE,
			}},
			want: endingcomponents.VerbalNoun,
		},
		{
			name: "Adjective",
			ec: endingcomponents.EndingComponents{&pb.EndingComponents{
				Degree: pb.Degree_DEGREE_SUPERLATIVE,
				Case:   pb.Case_CASE_NOMINATIVE,
				Number: pb.Number_NUMBER_SINGULAR,
				Gender: pb.Gender_GENDER_FEMININE,
			}},
			want: endingcomponents.Adjective,
		},
		{
			name: "Pronoun",
			ec: endingcomponents.EndingComponents{&pb.EndingComponents{
				Case:   pb.Case_CASE_NOMINATIVE,
				Number: pb.Number_NUMBER_SINGULAR,
				Gender: pb.Gender_GENDER_MASCULINE,
			}},
			want: endingcomponents.Pronoun,
		},
		{
			name: "Noun",
			ec: endingcomponents.EndingComponents{&pb.EndingComponents{
				Case:   pb.Case_CASE_NOMINATIVE,
				Number: pb.Number_NUMBER_SINGULAR,
			}},
			want: endingcomponents.Noun,
		},
		{
			name: "Adverb",
			ec: endingcomponents.EndingComponents{&pb.EndingComponents{
				Degree: pb.Degree_DEGREE_COMPARATIVE,
			}},
			want: endingcomponents.Adverb,
		},
		{
			name: "RegularWord",
			ec:   endingcomponents.EndingComponents{&pb.EndingComponents{}},
			want: endingcomponents.RegularWord,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			assert.Equal(t, tt.want, tt.ec.PartOfSpeech())
		})
	}
}
