package endingcomponents

import pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"

type Case pb.Case

var Cases = []Case{
	Case(pb.Case_CASE_NOMINATIVE),
	Case(pb.Case_CASE_VOCATIVE),
	Case(pb.Case_CASE_ACCUSATIVE),
	Case(pb.Case_CASE_GENITIVE),
	Case(pb.Case_CASE_DATIVE),
	Case(pb.Case_CASE_ABLATIVE),
}

type Number pb.Number

var Numbers = []Number{
	Number(pb.Number_NUMBER_SINGULAR),
	Number(pb.Number_NUMBER_PLURAL),
}

type Gender pb.Gender

var Genders = []Gender{
	Gender(pb.Gender_GENDER_MASCULINE),
	Gender(pb.Gender_GENDER_FEMININE),
	Gender(pb.Gender_GENDER_NEUTER),
}

type Tense pb.Tense

var Tenses = []Tense{
	Tense(pb.Tense_TENSE_PRESENT),
	Tense(pb.Tense_TENSE_IMPERFECT),
	Tense(pb.Tense_TENSE_FUTURE),
	Tense(pb.Tense_TENSE_PERFECT),
	Tense(pb.Tense_TENSE_PLUPERFECT),
	Tense(pb.Tense_TENSE_FUTURE_PERFECT),
}

type Voice pb.Voice

var Voices = []Voice{
	Voice(pb.Voice_VOICE_ACTIVE),
	Voice(pb.Voice_VOICE_PASSIVE),
	Voice(pb.Voice_VOICE_DEPONENT),
	Voice(pb.Voice_VOICE_SEMI_DEPONENT),
}

type Mood pb.Mood

var Moods = []Mood{
	Mood(pb.Mood_MOOD_INDICATIVE),
	Mood(pb.Mood_MOOD_SUBJUNCTIVE),
	Mood(pb.Mood_MOOD_IMPERATIVE),
	Mood(pb.Mood_MOOD_INFINITIVE),
	Mood(pb.Mood_MOOD_PARTICIPLE),
	Mood(pb.Mood_MOOD_GERUND),
	Mood(pb.Mood_MOOD_SUPINE),
}

type Person pb.Person

var Persons = []Person{
	Person(pb.Person_PERSON_FIRST),
	Person(pb.Person_PERSON_SECOND),
	Person(pb.Person_PERSON_THIRD),
}

type Degree pb.Degree

var Degrees = []Degree{
	Degree(pb.Degree_DEGREE_POSITIVE),
	Degree(pb.Degree_DEGREE_COMPARATIVE),
	Degree(pb.Degree_DEGREE_SUPERLATIVE),
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

// XXX: Could this be completely removed in future?
type EndingComponents struct {
	*pb.EndingComponents // pointer as is pointer in the question types
}

// PartOfSpeech returns the PartOfSpeech enum for the EndingComponents based on which fields are present.
func (e *EndingComponents) PartOfSpeech() PartOfSpeech {
	hasCase := e.Case != pb.Case_CASE_UNSPECIFIED
	hasNumber := e.Number != pb.Number_NUMBER_UNSPECIFIED
	hasGender := e.Gender != pb.Gender_GENDER_UNSPECIFIED
	hasTense := e.Tense != pb.Tense_TENSE_UNSPECIFIED
	hasVoice := e.Voice != pb.Voice_VOICE_UNSPECIFIED
	hasMood := e.Mood != pb.Mood_MOOD_UNSPECIFIED
	hasPerson := e.Person != pb.Person_PERSON_UNSPECIFIED
	hasDegree := e.Degree != pb.Degree_DEGREE_UNSPECIFIED

	if hasTense && hasVoice && hasMood && hasPerson && hasNumber {
		return Verb
	}

	if hasTense && hasVoice && hasMood && !hasPerson && !hasNumber && !hasCase && !hasGender && !hasDegree {
		return InfinitivePOS
	}

	if hasTense && hasVoice && hasMood && hasNumber && hasGender && hasCase {
		return ParticiplePOS
	}

	if (e.Mood == pb.Mood_MOOD_GERUND || e.Mood == pb.Mood_MOOD_SUPINE) && hasCase {
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
