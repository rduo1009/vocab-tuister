package configtui

import (
	"github.com/charmbracelet/bubbles/v2/help"
	"github.com/charmbracelet/bubbles/v2/textinput"
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

type model struct {
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

// Doesn't look like I need this, but keeping just in case
// func (m *model) ToggleSettingByText(pageTitle, internalName string) {
// 	for pageIndex, page := range m.wizard.Pages {
// 		if page.Title == pageTitle {
// 			for settingIndex, setting := range page.Settings {
// 				if setting.InternalName == internalName {
// 					m.wizard.Pages[pageIndex].Settings[settingIndex].Checked = !setting.Checked
// 					return
// 				}
// 			}
// 		}
// 	}
// }

func (m *model) ToggleSetting(pageIndex, optionIndex int) {
	m.wizard.Pages[pageIndex].Settings[optionIndex].Checked = !m.wizard.Pages[pageIndex].Settings[optionIndex].Checked
}

var wizard = SettingsWizard{
	Pages: []SettingsPage{
		{
			Title: "Verb exclusions", Settings: []Setting{
				{InternalName: "exclude-verbs", DisplayName: "All of them", Checked: false},
				{InternalName: "exclude-verb-first-conjugation", DisplayName: "First conjugation verbs", Checked: false},
				{InternalName: "exclude-verb-second-conjugation", DisplayName: "Second conjugation verbs", Checked: false},
				{InternalName: "exclude-verb-third-conjugation", DisplayName: "Third conjugation verbs", Checked: false},
				{InternalName: "exclude-verb-fourth-conjugation", DisplayName: "Fourth conjugation verbs", Checked: false},
				{InternalName: "exclude-verb-thirdio-conjugation", DisplayName: "Third -io verbs", Checked: false},
				{InternalName: "exclude-verb-irregular-conjugation", DisplayName: "Irregular verbs", Checked: false},
				{InternalName: "exclude-verb-present-active-indicative", DisplayName: "Present active indicative", Checked: false},
				{InternalName: "exclude-verb-imperfect-active-indicative", DisplayName: "Imperfect active indicative", Checked: false},
				{InternalName: "exclude-verb-perfect-active-indicative", DisplayName: "Perfect active indicative", Checked: false},
				{InternalName: "exclude-verb-pluperfect-active-indicative", DisplayName: "Pluperfect active indicative", Checked: false},
				{InternalName: "exclude-verb-present-active-infinitive", DisplayName: "Present active infinitive", Checked: false},
				{InternalName: "exclude-verb-present-active-imperative", DisplayName: "Present active imperative", Checked: false},
				{InternalName: "exclude-verb-imperfect-active-subjunctive", DisplayName: "Imperative active subjunctive", Checked: false},
				{InternalName: "exclude-verb-pluperfect-active-subjunctive", DisplayName: "Pluperfect active subjunctive", Checked: false},
				{InternalName: "exclude-verb-singular", DisplayName: "Singular number", Checked: false},
				{InternalName: "exclude-verb-plural", DisplayName: "Plural number", Checked: false},
				{InternalName: "exclude-verb-1st-person", DisplayName: "1st person", Checked: false},
				{InternalName: "exclude-verb-2nd-person", DisplayName: "2nd person", Checked: false},
				{InternalName: "exclude-verb-3rd-person", DisplayName: "3rd person", Checked: false},
			},
		},
		{
			Title: "Participle exclusions", Settings: []Setting{
				{InternalName: "exclude-participles", DisplayName: "All of them", Checked: false},
				{InternalName: "exclude-participle-present-active", DisplayName: "Present active", Checked: false},
				{InternalName: "exclude-participle-perfect-passive", DisplayName: "Perfect passive", Checked: false},
				{InternalName: "exclude-participle-masculine", DisplayName: "Masculine gender", Checked: false},
				{InternalName: "exclude-participle-feminine", DisplayName: "Feminine gender", Checked: false},
				{InternalName: "exclude-participle-neuter", DisplayName: "Neuter gender", Checked: false},
				{InternalName: "exclude-participle-nominative", DisplayName: "Nominative case", Checked: false},
				{InternalName: "exclude-participle-vocative", DisplayName: "Vocative case", Checked: false},
				{InternalName: "exclude-participle-accusative", DisplayName: "Accusative case", Checked: false},
				{InternalName: "exclude-participle-genitive", DisplayName: "Genitive case", Checked: false},
				{InternalName: "exclude-participle-dative", DisplayName: "Dative case", Checked: false},
				{InternalName: "exclude-participle-ablative", DisplayName: "Ablative case", Checked: false},
				{InternalName: "exclude-participle-singular", DisplayName: "Singular number", Checked: false},
				{InternalName: "exclude-participle-plural", DisplayName: "Plural number", Checked: false},
			},
		},
		{
			Title: "Noun exclusions", Settings: []Setting{
				{InternalName: "exclude-nouns", DisplayName: "All of them", Checked: false},
				{InternalName: "exclude-noun-first-declension", DisplayName: "First declension nouns", Checked: false},
				{InternalName: "exclude-noun-second-declension", DisplayName: "Second declension nouns", Checked: false},
				{InternalName: "exclude-noun-third-declension", DisplayName: "Third declension nouns", Checked: false},
				{InternalName: "exclude-noun-fourth-declension", DisplayName: "Fourth declension nouns", Checked: false},
				{InternalName: "exclude-noun-fifth-declension", DisplayName: "Fifth declension nouns", Checked: false},
				{InternalName: "exclude-noun-irregular-declension", DisplayName: "Irregular nouns", Checked: false},
				{InternalName: "exclude-noun-nominative", DisplayName: "Nominative case", Checked: false},
				{InternalName: "exclude-noun-vocative", DisplayName: "Vocative case", Checked: false},
				{InternalName: "exclude-noun-accusative", DisplayName: "Accusative case", Checked: false},
				{InternalName: "exclude-noun-genitive", DisplayName: "Genitive case", Checked: false},
				{InternalName: "exclude-noun-dative", DisplayName: "Dative case", Checked: false},
				{InternalName: "exclude-noun-ablative", DisplayName: "Ablative case", Checked: false},
				{InternalName: "exclude-noun-singular", DisplayName: "Singular number", Checked: false},
				{InternalName: "exclude-noun-plural", DisplayName: "Plural number", Checked: false},
			},
		},
		{
			Title: "Adjective exclusions", Settings: []Setting{
				{InternalName: "exclude-adjectives", DisplayName: "All of them", Checked: false},
				{InternalName: "exclude-adjective-212-declension", DisplayName: "First and second declension adjectives", Checked: false},
				{InternalName: "exclude-adjective-third-declension", DisplayName: "Third declension adjectives", Checked: false},
				{InternalName: "exclude-adjective-masculine", DisplayName: "Masculine gender", Checked: false},
				{InternalName: "exclude-adjective-feminine", DisplayName: "Feminine gender", Checked: false},
				{InternalName: "exclude-adjective-neuter", DisplayName: "Neuter gender", Checked: false},
				{InternalName: "exclude-adjective-nominative", DisplayName: "Nominative case", Checked: false},
				{InternalName: "exclude-adjective-vocative", DisplayName: "Vocative case", Checked: false},
				{InternalName: "exclude-adjective-accusative", DisplayName: "Accusative case", Checked: false},
				{InternalName: "exclude-adjective-genitive", DisplayName: "Genitive case", Checked: false},
				{InternalName: "exclude-adjective-dative", DisplayName: "Dative case", Checked: false},
				{InternalName: "exclude-adjective-ablative", DisplayName: "Ablative case", Checked: false},
				{InternalName: "exclude-adjective-singular", DisplayName: "Singular number", Checked: false},
				{InternalName: "exclude-adjective-plural", DisplayName: "Plural number", Checked: false},
				{InternalName: "exclude-adjective-positive", DisplayName: "Positive degree", Checked: false},
				{InternalName: "exclude-adjective-comparative", DisplayName: "Comparative degree", Checked: false},
				{InternalName: "exclude-adjective-superlative", DisplayName: "Superlative degree", Checked: false},
			},
		},
		{
			Title: "Adverb exclusions", Settings: []Setting{
				{InternalName: "exclude-adverbs", DisplayName: "All of them", Checked: false},
				{InternalName: "exclude-adverb-positive", DisplayName: "Positive degree", Checked: false},
				{InternalName: "exclude-adverb-comparative", DisplayName: "Comparative degree", Checked: false},
				{InternalName: "exclude-adverb-superlative", DisplayName: "Superlative degree", Checked: false},
			},
		},
		{
			Title: "Pronoun exclusions", Settings: []Setting{
				{InternalName: "exclude-pronouns", DisplayName: "All of them", Checked: false},
				{InternalName: "exclude-pronoun-masculine", DisplayName: "Masculine gender", Checked: false},
				{InternalName: "exclude-pronoun-feminine", DisplayName: "Feminine gender", Checked: false},
				{InternalName: "exclude-pronoun-neuter", DisplayName: "Neuter gender", Checked: false},
				{InternalName: "exclude-pronoun-nominative", DisplayName: "Nominative case", Checked: false},
				{InternalName: "exclude-pronoun-vocative", DisplayName: "Vocative case", Checked: false},
				{InternalName: "exclude-pronoun-accusative", DisplayName: "Accusative case", Checked: false},
				{InternalName: "exclude-pronoun-genitive", DisplayName: "Genitive case", Checked: false},
				{InternalName: "exclude-pronoun-dative", DisplayName: "Dative case", Checked: false},
				{InternalName: "exclude-pronoun-ablative", DisplayName: "Ablative case", Checked: false},
				{InternalName: "exclude-pronoun-singular", DisplayName: "Singular number", Checked: false},
				{InternalName: "exclude-pronoun-plural", DisplayName: "Plural number", Checked: false},
			},
		},
		{
			Title: "Regular word exclusions", Settings: []Setting{
				{InternalName: "exclude-regulars", DisplayName: "All of them", Checked: false},
			},
		},
		{
			Title: "Question types", Settings: []Setting{
				{InternalName: "include-typein-engtolat", DisplayName: "Type-in English to Latin questions", Checked: true},
				{InternalName: "include-typein-lattoeng", DisplayName: "Type-in Latin to English questions", Checked: true},
				{InternalName: "include-parse", DisplayName: "Parsing questions", Checked: true},
				{InternalName: "include-inflect", DisplayName: "Inflecting questions", Checked: true},
				{InternalName: "include-principal-parts", DisplayName: "Principal parts questions", Checked: true},
				{InternalName: "include-multiplechoice-engtolat", DisplayName: "Multiple choice English to Latin questions", Checked: true},
				{InternalName: "include-multiplechoice-lattoeng", DisplayName: "Multiple choice Latin to English questions", Checked: true},
			},
		},
	},
}

func InitialModel(filePath string) model { //nolint:revive
	ti := textinput.New()
	ti.SetWidth(20)
	ti.Placeholder = "Must be a positive integer"
	ti.CharLimit = 3
	ti.Focus()

	return model{
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