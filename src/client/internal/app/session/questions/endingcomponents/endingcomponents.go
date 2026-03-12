package endingcomponents

import "strings"

//go:generate go tool stringer -type=Case,Number,Gender,Tense,Voice,Mood,Person,Degree,PartOfSpeech -linecomment -output=endingcomponents_string.go

type Case int

const (
	UnknownCase Case = iota //
	Nominative              // nominative
	Vocative                // vocative
	Accusative              // accusative
	Genitive                // genitive
	Dative                  // dative
	Ablative                // ablative
)

var Cases = []Case{
	Nominative,
	Vocative,
	Accusative,
	Genitive,
	Dative,
	Ablative,
}

type Number int

const (
	UnknownNumber Number = iota //
	Singular                    // singular
	Plural                      // plural
)

var Numbers = []Number{
	Singular,
	Plural,
}

type Gender int

const (
	UnknownGender Gender = iota //
	Masculine                   // masculine
	Feminine                    // feminine
	Neuter                      // neuter
)

var Genders = []Gender{
	Masculine,
	Feminine,
	Neuter,
}

type Tense int

const (
	UnknownTense  Tense = iota //
	Present                    // present
	Imperfect                  // imperfect
	Future                     // future
	Perfect                    // perfect
	Pluperfect                 // pluperfect
	FuturePerfect              // future perfect
)

var Tenses = []Tense{
	Present,
	Imperfect,
	Future,
	Perfect,
	Pluperfect,
	FuturePerfect,
}

type Voice int

const (
	UnknownVoice Voice = iota //
	Active                    // active
	Passive                   // passive
	Deponent                  // deponent
	SemiDeponent              // semi-deponent
)

var Voices = []Voice{
	Active,
	Passive,
	Deponent,
	SemiDeponent,
}

type Mood int

const (
	UnknownMood    Mood = iota //
	Indicative                 // indicative
	Subjunctive                // subjunctive
	Imperative                 // imperative
	InfinitiveMood             // infinitive
	ParticipleMood             // participle
	Gerund                     // gerund
	Supine                     // supine
)

var Moods = []Mood{
	Indicative,
	Subjunctive,
	Imperative,
	InfinitiveMood,
	ParticipleMood,
	Gerund,
	Supine,
}

type Person int

const (
	UnknownPerson Person = iota //
	FirstPerson                 // 1st person
	SecondPerson                // 2nd person
	ThirdPerson                 // 3rd person
)

var Persons = []Person{
	FirstPerson,
	SecondPerson,
	ThirdPerson,
}

type Degree int

const (
	UnknownDegree Degree = iota //
	Positive                    // positive
	Comparative                 // comparative
	Superlative                 // superlative
)

var Degrees = []Degree{
	Positive,
	Comparative,
	Superlative,
}

type PartOfSpeech int

const (
	UnknownPartOfSpeech PartOfSpeech = iota //
	Noun                                    // noun
	Pronoun                                 // pronoun
	Adjective                               // adjective
	Verb                                    // verb
	VerbalNoun                              // verbal noun
	ParticiplePOS                           // participle
	InfinitivePOS                           // infinitive
	Adverb                                  // adverb
	RegularWord                             // regular word
)

type EndingComponents struct {
	Case   Case
	Number Number
	Gender Gender
	Tense  Tense
	Voice  Voice
	Mood   Mood
	Person Person
	Degree Degree
}

// PartOfSpeech returns the PartOfSpeech enum for the EndingComponents based on which fields are present.
func (e EndingComponents) PartOfSpeech() PartOfSpeech {
	hasCase := e.Case != UnknownCase
	hasNumber := e.Number != UnknownNumber
	hasGender := e.Gender != UnknownGender
	hasTense := e.Tense != UnknownTense
	hasVoice := e.Voice != UnknownVoice
	hasMood := e.Mood != UnknownMood
	hasPerson := e.Person != UnknownPerson
	hasDegree := e.Degree != UnknownDegree

	if hasTense && hasVoice && hasMood && hasPerson && hasNumber {
		return Verb
	}

	if hasTense && hasVoice && hasMood && !hasPerson && !hasNumber && !hasCase && !hasGender && !hasDegree {
		return InfinitivePOS
	}

	if hasTense && hasVoice && hasMood && hasNumber && hasGender && hasCase {
		return ParticiplePOS
	}

	if (e.Mood == Gerund || e.Mood == Supine) && hasCase {
		return VerbalNoun
	}

	if hasDegree && !hasCase && !hasNumber && !hasGender && !hasTense && !hasVoice && !hasMood && !hasPerson {
		return Adverb
	}

	if hasNumber && hasGender && hasCase && hasDegree {
		return Adjective
	}

	if hasNumber && hasGender && hasCase && !hasDegree && !hasTense && !hasVoice && !hasMood && !hasPerson {
		return Pronoun
	}

	if hasNumber && hasCase && !hasGender {
		return Noun
	}

	if !hasCase && !hasNumber && !hasGender && !hasTense && !hasVoice && !hasMood && !hasPerson && !hasDegree {
		return RegularWord
	}

	return UnknownPartOfSpeech
}

// String returns the string representation of the EndingComponents, akin to the .string property in the Python code.
func (e EndingComponents) String() string {
	pos := e.PartOfSpeech()
	switch pos {
	case Verb:
		return strings.Join([]string{
			e.Tense.String(), e.Voice.String(), e.Mood.String(), e.Number.String(), e.Person.String(),
		}, " ")

	case InfinitivePOS:
		return strings.Join([]string{
			e.Tense.String(), e.Voice.String(), e.Mood.String(),
		}, " ")

	case ParticiplePOS:
		if e.Tense == Future && e.Voice == Passive {
			return strings.Join([]string{
				"gerundive", e.Gender.String(), e.Case.String(), e.Number.String(),
			}, " ")
		}

		return strings.Join([]string{
			e.Tense.String(),
			e.Voice.String(),
			"participle",
			e.Gender.String(),
			e.Case.String(),
			e.Number.String(),
		}, " ")

	case VerbalNoun:
		return strings.Join([]string{
			e.Mood.String(), e.Case.String(),
		}, " ")

	case Adverb:
		return e.Degree.String() + " (adverb)"

	case Adjective:
		return strings.Join([]string{
			e.Degree.String(), e.Case.String(), e.Number.String(), e.Gender.String(),
		}, " ")

	case Pronoun:
		return strings.Join([]string{
			e.Case.String(), e.Number.String(), e.Gender.String(),
		}, " ")

	case Noun:
		return strings.Join([]string{
			e.Case.String(), e.Number.String(),
		}, " ")

	case RegularWord:
		return ""

	case UnknownPartOfSpeech:
		return "unknown"
	}

	panic("unreachable")
}
