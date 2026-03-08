package questions

import (
	"encoding/json/v2"
	"fmt"
	"strings"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions/endingcomponents"
)

// UnmarshalEndingComponents converts a verbose string into an EndingComponents struct.
func UnmarshalEndingComponents(s string) endingcomponents.EndingComponents {
	var ec endingcomponents.EndingComponents

	s = " " + s + " "

	for _, t := range []endingcomponents.Tense{
		endingcomponents.FuturePerfect,
		endingcomponents.Pluperfect,
		endingcomponents.Perfect,
		endingcomponents.Imperfect,
		endingcomponents.Future,
		endingcomponents.Present,
	} {
		if strings.Contains(s, " "+t.String()+" ") {
			ec.Tense = t
			s = strings.Replace(s, " "+t.String()+" ", " ", 1)
			break
		}
	}

	for _, p := range []endingcomponents.Person{
		endingcomponents.FirstPerson,
		endingcomponents.SecondPerson,
		endingcomponents.ThirdPerson,
	} {
		if strings.Contains(s, " "+p.String()+" ") {
			ec.Person = p
			s = strings.Replace(s, " "+p.String()+" ", " ", 1)
			break
		}
	}

	for _, c := range []endingcomponents.Case{
		endingcomponents.Nominative, endingcomponents.Vocative, endingcomponents.Accusative,
		endingcomponents.Genitive, endingcomponents.Dative, endingcomponents.Ablative,
	} {
		if strings.Contains(s, " "+c.String()+" ") {
			ec.Case = c
			s = strings.Replace(s, " "+c.String()+" ", " ", 1)
			break
		}
	}

	for _, n := range []endingcomponents.Number{
		endingcomponents.Singular, endingcomponents.Plural,
	} {
		if strings.Contains(s, " "+n.String()+" ") {
			ec.Number = n
			s = strings.Replace(s, " "+n.String()+" ", " ", 1)
			break
		}
	}

	for _, g := range []endingcomponents.Gender{
		endingcomponents.Masculine, endingcomponents.Feminine, endingcomponents.Neuter,
	} {
		if strings.Contains(s, " "+g.String()+" ") {
			ec.Gender = g
			s = strings.Replace(s, " "+g.String()+" ", " ", 1)
			break
		}
	}

	for _, v := range []endingcomponents.Voice{
		endingcomponents.SemiDeponent, endingcomponents.Deponent, endingcomponents.Passive, endingcomponents.Active,
	} {
		if strings.Contains(s, " "+v.String()+" ") {
			ec.Voice = v
			s = strings.Replace(s, " "+v.String()+" ", " ", 1)
			break
		}
	}

	for _, m := range []endingcomponents.Mood{
		endingcomponents.Indicative, endingcomponents.Subjunctive, endingcomponents.Imperative,
		endingcomponents.InfinitiveMood, endingcomponents.ParticipleMood, endingcomponents.Gerund, endingcomponents.Supine,
	} {
		if strings.Contains(s, " "+m.String()+" ") {
			ec.Mood = m
			s = strings.Replace(s, " "+m.String()+" ", " ", 1)
			break
		}
	}

	for _, d := range []endingcomponents.Degree{
		endingcomponents.Positive, endingcomponents.Comparative, endingcomponents.Superlative,
	} {
		if strings.Contains(s, " "+d.String()+" ") {
			ec.Degree = d
			break
		}
	}

	return ec
}

// UnmarshalQuestion unmarshals JSON into the appropriate Question type.
func UnmarshalQuestion(data []byte) (Question, error) {
	// First, peek at the question_type
	var wrapper struct {
		QuestionType string `json:"question_type"`
	}
	if err := json.Unmarshal(data, &wrapper); err != nil {
		return nil, fmt.Errorf("failed to unmarshal question_type: %w", err)
	}

	// Based on question_type, unmarshal into the appropriate concrete type
	switch wrapper.QuestionType {
	case "MultipleChoiceEngToLatQuestion":
		var q MultipleChoiceEngToLatQuestion
		if err := json.Unmarshal(data, &q); err != nil {
			return nil, fmt.Errorf("failed to unmarshal MultipleChoiceEngToLatQuestion: %w", err)
		}

		return &q, nil

	case "MultipleChoiceLatToEngQuestion":
		var q MultipleChoiceLatToEngQuestion
		if err := json.Unmarshal(data, &q); err != nil {
			return nil, fmt.Errorf("failed to unmarshal MultipleChoiceLatToEngQuestion: %w", err)
		}

		return &q, nil

	case "ParseWordCompToLatQuestion":
		var raw struct {
			Answers    []string `json:"answers"`
			Components string   `json:"components"`
			MainAnswer string   `json:"main_answer"`
			Prompt     string   `json:"prompt"`
		}
		if err := json.Unmarshal(data, &raw); err != nil {
			return nil, fmt.Errorf("failed to unmarshal ParseWordCompToLatQuestion: %w", err)
		}

		q := ParseWordCompToLatQuestion{
			Answers:    raw.Answers,
			Components: UnmarshalEndingComponents(raw.Components),
			MainAnswer: raw.MainAnswer,
			Prompt:     raw.Prompt,
		}

		return &q, nil

	case "ParseWordLatToCompQuestion":
		var raw struct {
			Answers         []map[string]string `json:"answers"`
			DictionaryEntry string              `json:"dictionary_entry"`
			MainAnswer      map[string]string   `json:"main_answer"`
			Prompt          string              `json:"prompt"`
		}
		if err := json.Unmarshal(data, &raw); err != nil {
			return nil, fmt.Errorf("failed to unmarshal ParseWordLatToCompQuestion: %w", err)
		}

		var answers []endingcomponents.EndingComponents
		for _, a := range raw.Answers {
			var parts []string
			for _, v := range a {
				parts = append(parts, v)
			}

			answers = append(answers, UnmarshalEndingComponents(strings.Join(parts, " ")))
		}

		var mainParts []string
		for _, v := range raw.MainAnswer {
			mainParts = append(mainParts, v)
		}

		q := ParseWordLatToCompQuestion{
			Answers:         answers,
			DictionaryEntry: raw.DictionaryEntry,
			MainAnswer:      UnmarshalEndingComponents(strings.Join(mainParts, " ")),
			Prompt:          raw.Prompt,
		}

		return &q, nil

	case "TypeInEngToLatQuestion":
		var q TypeInEngToLatQuestion
		if err := json.Unmarshal(data, &q); err != nil {
			return nil, fmt.Errorf("failed to unmarshal TypeInEngToLatQuestion: %w", err)
		}

		return &q, nil

	case "TypeInLatToEngQuestion":
		var q TypeInLatToEngQuestion
		if err := json.Unmarshal(data, &q); err != nil {
			return nil, fmt.Errorf("failed to unmarshal TypeInLatToEngQuestion: %w", err)
		}

		return &q, nil

	case "PrincipalPartsQuestion":
		var q PrincipalPartsQuestion
		if err := json.Unmarshal(data, &q); err != nil {
			return nil, fmt.Errorf("failed to unmarshal PrincipalPartsQuestion: %w", err)
		}

		return &q, nil

	default:
		return nil, fmt.Errorf("unknown question_type: %s", wrapper.QuestionType)
	}
}
