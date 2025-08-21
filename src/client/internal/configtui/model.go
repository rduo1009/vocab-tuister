package configtui

import (
	"github.com/charmbracelet/bubbles/help"
	"github.com/charmbracelet/bubbles/textinput"
)

type Setting struct {
	DisplayName  string
	InternalName string
	Checked      bool
}

type SettingsPage struct {
	Title    string
	Settings []Setting
}

type SettingsWizard struct {
	Pages []SettingsPage
}

type Model struct {
	wizard              SettingsWizard
	textinput           textinput.Model
	help                help.Model
	keys                KeyMap
	currentPage         int
	selectedOption      int
	mcOptionsNumberPage bool
	filePath            string
	width               int
	height              int
	err                 error
}

func (m *Model) toggleSetting(pageIndex, optionIndex int) {
	m.wizard.Pages[pageIndex].Settings[optionIndex].Checked = !m.wizard.Pages[pageIndex].Settings[optionIndex].Checked
}

var wizard = SettingsWizard{
	Pages: []SettingsPage{
		{
			Title: "Verb exclusions", Settings: []Setting{
				{"exclude-verbs", "All of them", false},
				{"exclude-deponents", "Deponent verbs", false},
				{"exclude-verb-first-conjugation", "First conjugation verbs", false},
				{"exclude-verb-second-conjugation", "Second conjugation verbs", false},
				{"exclude-verb-third-conjugation", "Third conjugation verbs", false},
				{"exclude-verb-fourth-conjugation", "Fourth conjugation verbs", false},
				{"exclude-verb-mixed-conjugation", "Mixed conjugation verbs", false},
				{"exclude-verb-irregular-conjugation", "Irregular verbs", false},
				{"exclude-verb-present-active-indicative", "Present active indicative", false},
				{"exclude-verb-imperfect-active-indicative", "Imperfect active indicative", false},
				{"exclude-verb-future-active-indicative", "Future active indicative", false},
				{"exclude-verb-perfect-active-indicative", "Perfect active indicative", false},
				{"exclude-verb-pluperfect-active-indicative", "Pluperfect active indicative", false},
				{
					"exclude-verb-future-perfect-active-indicative",
					"Future perfect active indicative",
					false,
				},
				{"exclude-verb-present-passive-indicative", "Present passive indicative", false},
				{"exclude-verb-imperfect-passive-indicative", "Imperfect passive indicative", false},
				{"exclude-verb-future-passive-indicative", "Future passive indicative", false},
				{"exclude-verb-perfect-passive-indicative", "Perfect passive indicative", false},
				{"exclude-verb-pluperfect-passive-indicative", "Pluperfect passive indicative", false},
				{
					"exclude-verb-future-perfect-passive-indicative",
					"Future perfect passive indicative",
					false,
				},
				{"exclude-verb-present-active-subjunctive", "Present active subjunctive", false},
				{"exclude-verb-imperfect-active-subjunctive", "Imperfect active subjunctive", false},
				{"exclude-verb-perfect-active-subjunctive", "Perfect active subjunctive", false},
				{"exclude-verb-pluperfect-active-subjunctive", "Pluperfect active subjunctive", false},
				{"exclude-verb-present-active-imperative", "Present active imperative", false},
				{"exclude-verb-future-active-imperative", "Future active imperative", false},
				{"exclude-verb-present-passive-imperative", "Present passive imperative", false},
				{"exclude-verb-future-passive-imperative", "Future passive imperative", false},
				{"exclude-verb-present-active-infinitive", "Present active infinitive", false},
				{"exclude-verb-future-active-infinitive", "Future active infinitive", false},
				{"exclude-verb-perfect-active-infinitive", "Perfect active infinitive", false},
				{"exclude-verb-present-passive-infinitive", "Present passive infinitive", false},
				{"exclude-verb-future-passive-infinitive", "Future passive infinitive", false},
				{"exclude-verb-perfect-passive-infinitive", "Perfect passive infinitive", false},
				{"exclude-verb-singular", "Singular number", false},
				{"exclude-verb-plural", "Plural number", false},
				{"exclude-verb-1st-person", "1st person", false},
				{"exclude-verb-2nd-person", "2nd person", false},
				{"exclude-verb-3rd-person", "3rd person", false},
			},
		},
		{
			Title: "Participle exclusions", Settings: []Setting{
				{"exclude-participles", "All of them", false},
				{"exclude-participle-present-active", "Present active", false},
				{"exclude-participle-perfect-passive", "Perfect passive", false},
				{"exclude-participle-future-active", "Future active", false},
				{"exclude-participle-masculine", "Masculine gender", false},
				{"exclude-participle-feminine", "Feminine gender", false},
				{"exclude-participle-neuter", "Neuter gender", false},
				{"exclude-participle-nominative", "Nominative case", false},
				{"exclude-participle-vocative", "Vocative case", false},
				{"exclude-participle-accusative", "Accusative case", false},
				{"exclude-participle-genitive", "Genitive case", false},
				{"exclude-participle-dative", "Dative case", false},
				{"exclude-participle-ablative", "Ablative case", false},
				{"exclude-participle-singular", "Singular number", false},
				{"exclude-participle-plural", "Plural number", false},
			},
		},
		{
			Title: "Other verb exclusions", Settings: []Setting{
				{"exclude-gerundives", "Gerundives", false},
				{"exclude-gerunds", "Gerunds", false},
				{"exclude-supines", "Supines", false},
			},
		},
		{
			Title: "Noun exclusions", Settings: []Setting{
				{"exclude-nouns", "All of them", false},
				{"exclude-noun-first-declension", "First declension nouns", false},
				{"exclude-noun-second-declension", "Second declension nouns", false},
				{"exclude-noun-third-declension", "Third declension nouns", false},
				{"exclude-noun-fourth-declension", "Fourth declension nouns", false},
				{"exclude-noun-fifth-declension", "Fifth declension nouns", false},
				{"exclude-noun-irregular-declension", "Irregular nouns", false},
				{"exclude-noun-nominative", "Nominative case", false},
				{"exclude-noun-vocative", "Vocative case", false},
				{"exclude-noun-accusative", "Accusative case", false},
				{"exclude-noun-genitive", "Genitive case", false},
				{"exclude-noun-dative", "Dative case", false},
				{"exclude-noun-ablative", "Ablative case", false},
				{"exclude-noun-singular", "Singular number", false},
				{"exclude-noun-plural", "Plural number", false},
			},
		},
		{
			Title: "Adjective exclusions", Settings: []Setting{
				{"exclude-adjectives", "All of them", false},
				{"exclude-adjective-212-declension", "First and second declension adjectives", false},
				{"exclude-adjective-third-declension", "Third declension adjectives", false},
				{"exclude-adjective-masculine", "Masculine gender", false},
				{"exclude-adjective-feminine", "Feminine gender", false},
				{"exclude-adjective-neuter", "Neuter gender", false},
				{"exclude-adjective-nominative", "Nominative case", false},
				{"exclude-adjective-vocative", "Vocative case", false},
				{"exclude-adjective-accusative", "Accusative case", false},
				{"exclude-adjective-genitive", "Genitive case", false},
				{"exclude-adjective-dative", "Dative case", false},
				{"exclude-adjective-ablative", "Ablative case", false},
				{"exclude-adjective-singular", "Singular number", false},
				{"exclude-adjective-plural", "Plural number", false},
				{"exclude-adjective-positive", "Positive degree", false},
				{"exclude-adjective-comparative", "Comparative degree", false},
				{"exclude-adjective-superlative", "Superlative degree", false},
			},
		},
		{
			Title: "Adverb exclusions", Settings: []Setting{
				{"exclude-adverbs", "All of them", false},
				{"exclude-adverb-positive", "Positive degree", false},
				{"exclude-adverb-comparative", "Comparative degree", false},
				{"exclude-adverb-superlative", "Superlative degree", false},
			},
		},
		{
			Title: "Pronoun exclusions", Settings: []Setting{
				{"exclude-pronouns", "All of them", false},
				{"exclude-pronoun-masculine", "Masculine gender", false},
				{"exclude-pronoun-feminine", "Feminine gender", false},
				{"exclude-pronoun-neuter", "Neuter gender", false},
				{"exclude-pronoun-nominative", "Nominative case", false},
				{"exclude-pronoun-vocative", "Vocative case", false},
				{"exclude-pronoun-accusative", "Accusative case", false},
				{"exclude-pronoun-genitive", "Genitive case", false},
				{"exclude-pronoun-dative", "Dative case", false},
				{"exclude-pronoun-ablative", "Ablative case", false},
				{"exclude-pronoun-singular", "Singular number", false},
				{"exclude-pronoun-plural", "Plural number", false},
			},
		},
		{
			Title: "Regular word exclusions", Settings: []Setting{
				{"exclude-regulars", "All of them", false},
			},
		},
		{
			Title: "Miscellaneous settings", Settings: []Setting{
				{"english-subjunctives", "English translations of subjunctive verbs", false},
				{
					"english-verbal-nouns",
					"English translations of verbal nouns (gerunds/supines)",
					false,
				},
			},
		},
		{
			Title: "Question types", Settings: []Setting{
				{"include-typein-engtolat", "Type-in English to Latin questions", true},
				{"include-typein-lattoeng", "Type-in Latin to English questions", true},
				{"include-parse", "Parsing questions", true},
				{"include-inflect", "Inflecting questions", true},
				{"include-principal-parts", "Principal parts questions", true},
				{"include-multiplechoice-engtolat", "Multiple choice English to Latin questions", true},
				{"include-multiplechoice-lattoeng", "Multiple choice Latin to English questions", true},
			},
		},
	},
}

func InitialModel(filePath string) Model {
	ti := textinput.New()
	ti.Width = 20
	ti.Placeholder = "Must be a positive integer"
	ti.CharLimit = 3
	ti.Focus()

	return Model{
		wizard:              wizard,
		textinput:           ti,
		help:                help.New(),
		keys:                DefaultKeyMap,
		currentPage:         0,
		selectedOption:      0,
		mcOptionsNumberPage: false,
		filePath:            filePath,
		err:                 nil,
	}
}
