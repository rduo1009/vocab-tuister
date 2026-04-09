package config

import (
	"errors"
	"strconv"

	"charm.land/huh/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

// XXX: Would https://github.com/charmbracelet/huh/pull/195 be relevant??

type formValues struct {
	PartsOfSpeechExclusions []string
	VerbExclusions          []string
	ParticipleExclusions    []string
	OtherVerbExclusions     []string
	NounExclusions          []string
	AdjectiveExclusions     []string
	AdverbExclusions        []string
	PronounExclusions       []string
	RegularExclusions       []string
	Miscellaneous           []string
	QuestionTypes           []string

	NumberMultipleChoiceOptionsString string
	NumberOfQuestionsString           string
}

var allKeys = []string{
	"english-subjunctives",
	"english-verbal-nouns",
	"exclude-adjective-212-declension",
	"exclude-adjective-ablative",
	"exclude-adjective-accusative",
	"exclude-adjective-comparative",
	"exclude-adjective-dative",
	"exclude-adjective-feminine",
	"exclude-adjective-genitive",
	"exclude-adjective-masculine",
	"exclude-adjective-neuter",
	"exclude-adjective-nominative",
	"exclude-adjective-plural",
	"exclude-adjective-positive",
	"exclude-adjective-singular",
	"exclude-adjective-superlative",
	"exclude-adjective-third-declension",
	"exclude-adjective-vocative",
	"exclude-adjectives",
	"exclude-adverb-comparative",
	"exclude-adverb-positive",
	"exclude-adverb-superlative",
	"exclude-adverbs",
	"exclude-deponents",
	"exclude-gerundives",
	"exclude-gerunds",
	"exclude-noun-ablative",
	"exclude-noun-accusative",
	"exclude-noun-dative",
	"exclude-noun-fifth-declension",
	"exclude-noun-first-declension",
	"exclude-noun-fourth-declension",
	"exclude-noun-genitive",
	"exclude-noun-irregular-declension",
	"exclude-noun-nominative",
	"exclude-noun-plural",
	"exclude-noun-second-declension",
	"exclude-noun-singular",
	"exclude-noun-third-declension",
	"exclude-noun-vocative",
	"exclude-nouns",
	"exclude-participle-ablative",
	"exclude-participle-accusative",
	"exclude-participle-dative",
	"exclude-participle-feminine",
	"exclude-participle-future-active",
	"exclude-participle-genitive",
	"exclude-participle-masculine",
	"exclude-participle-neuter",
	"exclude-participle-nominative",
	"exclude-participle-perfect-passive",
	"exclude-participle-plural",
	"exclude-participle-present-active",
	"exclude-participle-singular",
	"exclude-participle-vocative",
	"exclude-participles",
	"exclude-pronoun-ablative",
	"exclude-pronoun-accusative",
	"exclude-pronoun-dative",
	"exclude-pronoun-feminine",
	"exclude-pronoun-genitive",
	"exclude-pronoun-masculine",
	"exclude-pronoun-neuter",
	"exclude-pronoun-nominative",
	"exclude-pronoun-plural",
	"exclude-pronoun-singular",
	"exclude-pronoun-vocative",
	"exclude-pronouns",
	"exclude-regulars",
	"exclude-semi-deponents",
	"exclude-supines",
	"exclude-verb-1st-person",
	"exclude-verb-2nd-person",
	"exclude-verb-3rd-person",
	"exclude-verb-first-conjugation",
	"exclude-verb-fourth-conjugation",
	"exclude-verb-future-active-imperative",
	"exclude-verb-future-active-indicative",
	"exclude-verb-future-active-infinitive",
	"exclude-verb-future-passive-imperative",
	"exclude-verb-future-passive-indicative",
	"exclude-verb-future-passive-infinitive",
	"exclude-verb-future-perfect-active-indicative",
	"exclude-verb-future-perfect-passive-indicative",
	"exclude-verb-imperfect-active-indicative",
	"exclude-verb-imperfect-active-subjunctive",
	"exclude-verb-imperfect-passive-indicative",
	"exclude-verb-irregular-conjugation",
	"exclude-verb-mixed-conjugation",
	"exclude-verb-perfect-active-indicative",
	"exclude-verb-perfect-active-infinitive",
	"exclude-verb-perfect-active-subjunctive",
	"exclude-verb-perfect-passive-indicative",
	"exclude-verb-perfect-passive-infinitive",
	"exclude-verb-pluperfect-active-indicative",
	"exclude-verb-pluperfect-active-subjunctive",
	"exclude-verb-pluperfect-passive-indicative",
	"exclude-verb-plural",
	"exclude-verb-present-active-imperative",
	"exclude-verb-present-active-indicative",
	"exclude-verb-present-active-infinitive",
	"exclude-verb-present-active-subjunctive",
	"exclude-verb-present-passive-imperative",
	"exclude-verb-present-passive-indicative",
	"exclude-verb-present-passive-infinitive",
	"exclude-verb-second-conjugation",
	"exclude-verb-singular",
	"exclude-verb-third-conjugation",
	"exclude-verbs",
	"include-inflect",
	"include-multiplechoice-engtolat",
	"include-multiplechoice-lattoeng",
	"include-parse",
	"include-principal-parts",
	"include-typein-engtolat",
	"include-typein-lattoeng",
}

func defaultForm() (*huh.Form, *formValues) {
	// Default values
	values := &formValues{
		NumberMultipleChoiceOptionsString: "3",
		NumberOfQuestionsString:           "50",
	}

	form := huh.NewForm(
		huh.NewGroup(
			huh.NewMultiSelect[string]().
				Title("Parts of speech exclusions").
				Options(
					huh.NewOption("Exclude verbs", "exclude-verbs"),
					huh.NewOption("Exclude participles", "exclude-participles"),
					huh.NewOption("Exclude nouns", "exclude-nouns"),
					huh.NewOption("Exclude adjectives", "exclude-adjectives"),
					huh.NewOption("Exclude adverbs", "exclude-adverbs"),
					huh.NewOption("Exclude pronouns", "exclude-pronouns"),
					huh.NewOption("Exclude regular words", "exclude-regulars"),
				).
				Value(&values.PartsOfSpeechExclusions),
		),
		huh.NewGroup(
			huh.NewMultiSelect[string]().
				Title("Verb exclusions").
				Options(
					huh.NewOption("Deponent verbs", "exclude-deponents"),
					huh.NewOption("Semi-deponent verbs", "exclude-semi-deponents"),
					huh.NewOption("First conjugation verbs", "exclude-verb-first-conjugation"),
					huh.NewOption("Second conjugation verbs", "exclude-verb-second-conjugation"),
					huh.NewOption("Third conjugation verbs", "exclude-verb-third-conjugation"),
					huh.NewOption("Fourth conjugation verbs", "exclude-verb-fourth-conjugation"),
					huh.NewOption("Mixed conjugation verbs", "exclude-verb-mixed-conjugation"),
					huh.NewOption("Irregular verbs", "exclude-verb-irregular-conjugation"),
					huh.NewOption("Present active indicative", "exclude-verb-present-active-indicative"),
					huh.NewOption("Imperfect active indicative", "exclude-verb-imperfect-active-indicative"),
					huh.NewOption("Future active indicative", "exclude-verb-future-active-indicative"),
					huh.NewOption("Perfect active indicative", "exclude-verb-perfect-active-indicative"),
					huh.NewOption("Pluperfect active indicative", "exclude-verb-pluperfect-active-indicative"),
					huh.NewOption("Future perfect active indicative", "exclude-verb-future-perfect-active-indicative"),
					huh.NewOption("Present passive indicative", "exclude-verb-present-passive-indicative"),
					huh.NewOption("Imperfect passive indicative", "exclude-verb-imperfect-passive-indicative"),
					huh.NewOption("Future passive indicative", "exclude-verb-future-passive-indicative"),
					huh.NewOption("Perfect passive indicative", "exclude-verb-perfect-passive-indicative"),
					huh.NewOption("Pluperfect passive indicative", "exclude-verb-pluperfect-passive-indicative"),
					huh.NewOption("Future perfect passive indicative", "exclude-verb-future-perfect-passive-indicative"),
					huh.NewOption("Present active subjunctive", "exclude-verb-present-active-subjunctive"),
					huh.NewOption("Imperfect active subjunctive", "exclude-verb-imperfect-active-subjunctive"),
					huh.NewOption("Perfect active subjunctive", "exclude-verb-perfect-active-subjunctive"),
					huh.NewOption("Pluperfect active subjunctive", "exclude-verb-pluperfect-active-subjunctive"),
					huh.NewOption("Present active imperative", "exclude-verb-present-active-imperative"),
					huh.NewOption("Future active imperative", "exclude-verb-future-active-imperative"),
					huh.NewOption("Present passive imperative", "exclude-verb-present-passive-imperative"),
					huh.NewOption("Future passive imperative", "exclude-verb-future-passive-imperative"),
					huh.NewOption("Present active infinitive", "exclude-verb-present-active-infinitive"),
					huh.NewOption("Future active infinitive", "exclude-verb-future-active-infinitive"),
					huh.NewOption("Perfect active infinitive", "exclude-verb-perfect-active-infinitive"),
					huh.NewOption("Present passive infinitive", "exclude-verb-present-passive-infinitive"),
					huh.NewOption("Future passive infinitive", "exclude-verb-future-passive-infinitive"),
					huh.NewOption("Perfect passive infinitive", "exclude-verb-perfect-passive-infinitive"),
					huh.NewOption("Singular number", "exclude-verb-singular"),
					huh.NewOption("Plural number", "exclude-verb-plural"),
					huh.NewOption("1st person", "exclude-verb-1st-person"),
					huh.NewOption("2nd person", "exclude-verb-2nd-person"),
					huh.NewOption("3rd person", "exclude-verb-3rd-person"),
				).
				Value(&values.VerbExclusions),
			huh.NewMultiSelect[string]().
				Title("Participle exclusions").
				Options(
					huh.NewOption("Present active", "exclude-participle-present-active"),
					huh.NewOption("Perfect passive", "exclude-participle-perfect-passive"),
					huh.NewOption("Future active", "exclude-participle-future-active"),
					huh.NewOption("Masculine gender", "exclude-participle-masculine"),
					huh.NewOption("Feminine gender", "exclude-participle-feminine"),
					huh.NewOption("Neuter gender", "exclude-participle-neuter"),
					huh.NewOption("Nominative case", "exclude-participle-nominative"),
					huh.NewOption("Vocative case", "exclude-participle-vocative"),
					huh.NewOption("Accusative case", "exclude-participle-accusative"),
					huh.NewOption("Genitive case", "exclude-participle-genitive"),
					huh.NewOption("Dative case", "exclude-participle-dative"),
					huh.NewOption("Ablative case", "exclude-participle-ablative"),
					huh.NewOption("Singular number", "exclude-participle-singular"),
					huh.NewOption("Plural number", "exclude-participle-plural"),
				).
				Value(&values.ParticipleExclusions),
			huh.NewMultiSelect[string]().
				Title("Other verb exclusions").
				Options(
					huh.NewOption("Gerundives", "exclude-gerundives"),
					huh.NewOption("Gerunds", "exclude-gerunds"),
					huh.NewOption("Supines", "exclude-supines"),
				).
				Value(&values.OtherVerbExclusions),
		),
		huh.NewGroup(
			huh.NewMultiSelect[string]().
				Title("Noun exclusions").
				Options(
					huh.NewOption("First declension nouns", "exclude-noun-first-declension"),
					huh.NewOption("Second declension nouns", "exclude-noun-second-declension"),
					huh.NewOption("Third declension nouns", "exclude-noun-third-declension"),
					huh.NewOption("Fourth declension nouns", "exclude-noun-fourth-declension"),
					huh.NewOption("Fifth declension nouns", "exclude-noun-fifth-declension"),
					huh.NewOption("Irregular nouns", "exclude-noun-irregular-declension"),
					huh.NewOption("Nominative case", "exclude-noun-nominative"),
					huh.NewOption("Vocative case", "exclude-noun-vocative"),
					huh.NewOption("Accusative case", "exclude-noun-accusative"),
					huh.NewOption("Genitive case", "exclude-noun-genitive"),
					huh.NewOption("Dative case", "exclude-noun-dative"),
					huh.NewOption("Ablative case", "exclude-noun-ablative"),
					huh.NewOption("Singular number", "exclude-noun-singular"),
					huh.NewOption("Plural number", "exclude-noun-plural"),
				).
				Value(&values.NounExclusions),
		),
		huh.NewGroup(
			huh.NewMultiSelect[string]().
				Title("Adjective exclusions").
				Options(
					huh.NewOption("First and second declension adjectives", "exclude-adjective-212-declension"),
					huh.NewOption("Third declension adjectives", "exclude-adjective-third-declension"),
					huh.NewOption("Masculine gender", "exclude-adjective-masculine"),
					huh.NewOption("Feminine gender", "exclude-adjective-feminine"),
					huh.NewOption("Neuter gender", "exclude-adjective-neuter"),
					huh.NewOption("Nominative case", "exclude-adjective-nominative"),
					huh.NewOption("Vocative case", "exclude-adjective-vocative"),
					huh.NewOption("Accusative case", "exclude-adjective-accusative"),
					huh.NewOption("Genitive case", "exclude-adjective-genitive"),
					huh.NewOption("Dative case", "exclude-adjective-dative"),
					huh.NewOption("Ablative case", "exclude-adjective-ablative"),
					huh.NewOption("Singular number", "exclude-adjective-singular"),
					huh.NewOption("Plural number", "exclude-adjective-plural"),
					huh.NewOption("Positive degree", "exclude-adjective-positive"),
					huh.NewOption("Comparative degree", "exclude-adjective-comparative"),
					huh.NewOption("Superlative degree", "exclude-adjective-superlative"),
				).
				Value(&values.AdjectiveExclusions),
			huh.NewMultiSelect[string]().
				Title("Adverb exclusions").
				Options(
					huh.NewOption("Positive degree", "exclude-adverb-positive"),
					huh.NewOption("Comparative degree", "exclude-adverb-comparative"),
					huh.NewOption("Superlative degree", "exclude-adverb-superlative"),
				).
				Value(&values.AdverbExclusions),
		),
		huh.NewGroup(
			huh.NewMultiSelect[string]().
				Title("Pronoun exclusions").
				Options(
					huh.NewOption("Masculine gender", "exclude-pronoun-masculine"),
					huh.NewOption("Feminine gender", "exclude-pronoun-feminine"),
					huh.NewOption("Neuter gender", "exclude-pronoun-neuter"),
					huh.NewOption("Nominative case", "exclude-pronoun-nominative"),
					huh.NewOption("Vocative case", "exclude-pronoun-vocative"),
					huh.NewOption("Accusative case", "exclude-pronoun-accusative"),
					huh.NewOption("Genitive case", "exclude-pronoun-genitive"),
					huh.NewOption("Dative case", "exclude-pronoun-dative"),
					huh.NewOption("Ablative case", "exclude-pronoun-ablative"),
					huh.NewOption("Singular number", "exclude-pronoun-singular"),
					huh.NewOption("Plural number", "exclude-pronoun-plural"),
				).
				Value(&values.PronounExclusions),
		),
		huh.NewGroup(
			huh.NewMultiSelect[string]().
				Title("Miscellaneous").
				Options(
					huh.NewOption("English translations of subjunctive verbs", "english-subjunctives"),
					huh.NewOption("English translations of verbal nouns (gerunds/supines)", "english-verbal-nouns"),
				).
				Value(&values.Miscellaneous),
		),
		huh.NewGroup(
			huh.NewMultiSelect[string]().
				Title("Question types").
				Options(
					huh.NewOption("Type-in English to Latin", "include-typein-engtolat").
						Selected(true),
					huh.NewOption("Type-in Latin to English", "include-typein-lattoeng").
						Selected(true),
					huh.NewOption("Parsing", "include-parse").Selected(true),
					huh.NewOption("Inflecting", "include-inflect").Selected(true),
					huh.NewOption("Principal parts", "include-principal-parts").Selected(true),
					huh.NewOption("Multiple choice English to Latin", "include-multiplechoice-engtolat").
						Selected(true),
					huh.NewOption("Multiple choice Latin to English", "include-multiplechoice-lattoeng").
						Selected(true),
				).
				Value(&values.QuestionTypes),
			huh.NewInput().
				Title("Number of options in multiple choice questions").
				Value(&values.NumberMultipleChoiceOptionsString).
				Validate(func(str string) error {
					_, err := strconv.Atoi(str)
					if err != nil {
						return errors.New("must be an integer")
					}
					return nil
				}),
			huh.NewInput().
				Title("Number of questions").
				Value(&values.NumberOfQuestionsString).
				Validate(func(str string) error {
					_, err := strconv.Atoi(str)
					if err != nil {
						return errors.New("must be an integer")
					}
					return nil
				}),
		),
	)

	form.SubmitCmd = util.MsgCmd(formSubmittedMsg{})

	return form, values
}
