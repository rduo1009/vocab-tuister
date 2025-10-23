package config

import "github.com/rduo1009/vocab-tuister/src/client/internal/types/modes"

type Option struct {
	InternalName string
	DisplayName  string

	Type          modes.OptionType
	BoolValue     bool
	TextValue     string
	NumberValue   int
	SelectValue   string
	SelectOptions []string // for dropdowns
}

type SessionConfigPage struct {
	Title   string
	Options []Option
}

type SessionConfigWizard struct {
	Pages []SessionConfigPage
}

var wizard = SessionConfigWizard{
	Pages: []SessionConfigPage{
		{
			Title: "Verb exclusions", Options: []Option{
				{Type: modes.OptionBool, InternalName: "exclude-verbs", DisplayName: "All of them", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-deponents", DisplayName: "Deponent verbs", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-first-conjugation", DisplayName: "First conjugation verbs", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-second-conjugation", DisplayName: "Second conjugation verbs", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-third-conjugation", DisplayName: "Third conjugation verbs", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-fourth-conjugation", DisplayName: "Fourth conjugation verbs", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-mixed-conjugation", DisplayName: "Mixed conjugation verbs", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-irregular-conjugation", DisplayName: "Irregular verbs", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-present-active-indicative", DisplayName: "Present active indicative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-imperfect-active-indicative", DisplayName: "Imperfect active indicative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-future-active-indicative", DisplayName: "Future active indicative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-perfect-active-indicative", DisplayName: "Perfect active indicative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-pluperfect-active-indicative", DisplayName: "Pluperfect active indicative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-future-perfect-active-indicative", DisplayName: "Future perfect active indicative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-present-passive-indicative", DisplayName: "Present passive indicative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-imperfect-passive-indicative", DisplayName: "Imperfect passive indicative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-future-passive-indicative", DisplayName: "Future passive indicative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-perfect-passive-indicative", DisplayName: "Perfect passive indicative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-pluperfect-passive-indicative", DisplayName: "Pluperfect passive indicative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-future-perfect-passive-indicative", DisplayName: "Future perfect passive indicative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-present-active-subjunctive", DisplayName: "Present active subjunctive", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-imperfect-active-subjunctive", DisplayName: "Imperfect active subjunctive", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-perfect-active-subjunctive", DisplayName: "Perfect active subjunctive", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-pluperfect-active-subjunctive", DisplayName: "Pluperfect active subjunctive", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-present-active-imperative", DisplayName: "Present active imperative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-future-active-imperative", DisplayName: "Future active imperative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-present-passive-imperative", DisplayName: "Present passive imperative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-future-passive-imperative", DisplayName: "Future passive imperative", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-present-active-infinitive", DisplayName: "Present active infinitive", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-future-active-infinitive", DisplayName: "Future active infinitive", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-perfect-active-infinitive", DisplayName: "Perfect active infinitive", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-present-passive-infinitive", DisplayName: "Present passive infinitive", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-future-passive-infinitive", DisplayName: "Future passive infinitive", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-perfect-passive-infinitive", DisplayName: "Perfect passive infinitive", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-singular", DisplayName: "Singular number", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-plural", DisplayName: "Plural number", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-1st-person", DisplayName: "1st person", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-2nd-person", DisplayName: "2nd person", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-verb-3rd-person", DisplayName: "3rd person", BoolValue: false},
			},
		},
		{ //nolint:dupl
			Title: "Participle exclusions", Options: []Option{
				{Type: modes.OptionBool, InternalName: "exclude-participles", DisplayName: "All of them", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-participle-present-active", DisplayName: "Present active", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-participle-perfect-passive", DisplayName: "Perfect passive", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-participle-future-active", DisplayName: "Future active", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-participle-masculine", DisplayName: "Masculine gender", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-participle-feminine", DisplayName: "Feminine gender", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-participle-neuter", DisplayName: "Neuter gender", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-participle-nominative", DisplayName: "Nominative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-participle-vocative", DisplayName: "Vocative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-participle-accusative", DisplayName: "Accusative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-participle-genitive", DisplayName: "Genitive case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-participle-dative", DisplayName: "Dative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-participle-ablative", DisplayName: "Ablative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-participle-singular", DisplayName: "Singular number", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-participle-plural", DisplayName: "Plural number", BoolValue: false},
			},
		},
		{
			Title: "Other verb exclusions", Options: []Option{
				{Type: modes.OptionBool, InternalName: "exclude-gerundives", DisplayName: "Gerundives", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-gerunds", DisplayName: "Gerunds", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-supines", DisplayName: "Supines", BoolValue: false},
			},
		},
		{ //nolint:dupl
			Title: "Noun exclusions", Options: []Option{
				{Type: modes.OptionBool, InternalName: "exclude-nouns", DisplayName: "All of them", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-noun-first-declension", DisplayName: "First declension nouns", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-noun-second-declension", DisplayName: "Second declension nouns", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-noun-third-declension", DisplayName: "Third declension nouns", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-noun-fourth-declension", DisplayName: "Fourth declension nouns", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-noun-fifth-declension", DisplayName: "Fifth declension nouns", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-noun-irregular-declension", DisplayName: "Irregular nouns", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-noun-nominative", DisplayName: "Nominative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-noun-vocative", DisplayName: "Vocative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-noun-accusative", DisplayName: "Accusative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-noun-genitive", DisplayName: "Genitive case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-noun-dative", DisplayName: "Dative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-noun-ablative", DisplayName: "Ablative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-noun-singular", DisplayName: "Singular number", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-noun-plural", DisplayName: "Plural number", BoolValue: false},
			},
		},
		{
			Title: "Adjective exclusions", Options: []Option{
				{Type: modes.OptionBool, InternalName: "exclude-adjectives", DisplayName: "All of them", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-212-declension", DisplayName: "First and second declension adjectives", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-third-declension", DisplayName: "Third declension adjectives", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-masculine", DisplayName: "Masculine gender", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-feminine", DisplayName: "Feminine gender", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-neuter", DisplayName: "Neuter gender", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-nominative", DisplayName: "Nominative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-vocative", DisplayName: "Vocative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-accusative", DisplayName: "Accusative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-genitive", DisplayName: "Genitive case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-dative", DisplayName: "Dative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-ablative", DisplayName: "Ablative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-singular", DisplayName: "Singular number", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-plural", DisplayName: "Plural number", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-positive", DisplayName: "Positive degree", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-comparative", DisplayName: "Comparative degree", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adjective-superlative", DisplayName: "Superlative degree", BoolValue: false},
			},
		},
		{
			Title: "Adverb exclusions", Options: []Option{
				{Type: modes.OptionBool, InternalName: "exclude-adverbs", DisplayName: "All of them", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adverb-positive", DisplayName: "Positive degree", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adverb-comparative", DisplayName: "Comparative degree", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-adverb-superlative", DisplayName: "Superlative degree", BoolValue: false},
			},
		},
		{
			Title: "Pronoun exclusions", Options: []Option{
				{Type: modes.OptionBool, InternalName: "exclude-pronouns", DisplayName: "All of them", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-pronoun-masculine", DisplayName: "Masculine gender", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-pronoun-feminine", DisplayName: "Feminine gender", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-pronoun-neuter", DisplayName: "Neuter gender", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-pronoun-nominative", DisplayName: "Nominative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-pronoun-vocative", DisplayName: "Vocative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-pronoun-accusative", DisplayName: "Accusative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-pronoun-genitive", DisplayName: "Genitive case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-pronoun-dative", DisplayName: "Dative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-pronoun-ablative", DisplayName: "Ablative case", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-pronoun-singular", DisplayName: "Singular number", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "exclude-pronoun-plural", DisplayName: "Plural number", BoolValue: false},
			},
		},
		{
			Title: "Regular word exclusions", Options: []Option{
				{Type: modes.OptionBool, InternalName: "exclude-regulars", DisplayName: "All of them", BoolValue: false},
			},
		},
		{
			Title: "Miscellaneous", Options: []Option{
				{Type: modes.OptionBool, InternalName: "english-subjunctives", DisplayName: "English translations of subjunctive verbs", BoolValue: false},
				{Type: modes.OptionBool, InternalName: "english-verbal-nouns", DisplayName: "English translations of verbal nouns (gerunds/supines)", BoolValue: false},
			},
		},
		{
			Title: "Questions", Options: []Option{
				{Type: modes.OptionBool, InternalName: "include-typein-engtolat", DisplayName: "Type-in English to Latin", BoolValue: true},
				{Type: modes.OptionBool, InternalName: "include-typein-lattoeng", DisplayName: "Type-in Latin to English", BoolValue: true},
				{Type: modes.OptionBool, InternalName: "include-parse", DisplayName: "Parsing", BoolValue: true},
				{Type: modes.OptionBool, InternalName: "include-inflect", DisplayName: "Inflecting", BoolValue: true},
				{Type: modes.OptionBool, InternalName: "include-principal-parts", DisplayName: "Principal parts", BoolValue: true},
				{Type: modes.OptionBool, InternalName: "include-multiplechoice-engtolat", DisplayName: "Multiple choice English to Latin", BoolValue: true},
				{Type: modes.OptionBool, InternalName: "include-multiplechoice-lattoeng", DisplayName: "Multiple choice Latin to English", BoolValue: true},
			},
		},
		{
			Title: "Question config", Options: []Option{
				{Type: modes.OptionNumber, InternalName: "number-multiplechoice-options", DisplayName: "Number of options in multiple choice questions", NumberValue: 3},
				{Type: modes.OptionNumber, InternalName: "number-of-questions", DisplayName: "Number of questions", NumberValue: 50},
			},
		},
	},
}
