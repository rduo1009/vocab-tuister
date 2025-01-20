package enums

type Number int

const (
	Singular Number = iota
	Plural
)

type Tense int

const (
	Present Tense = iota
	Imperfect
	Future
	Perfect
	Pluperfect
	FuturePerfect
)

type Voice int

const (
	Active Voice = iota
	Passive
)

type Mood int

const (
	Indicative Mood = iota
	Infinitive
	Imperative
	Subjunctive
	Participle
)

type Case int

const (
	Nominative Case = iota
	Vocative
	Accusative
	Genitive
	Dative
	Ablative
)

type Gender int

const (
	Masculine Gender = iota
	Feminine
	Neuter
)

type Degree int

const (
	Positive Degree = iota
	Comparative
	Superlative
)
