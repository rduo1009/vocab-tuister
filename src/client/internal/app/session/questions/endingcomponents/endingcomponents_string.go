package endingcomponents

import pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"

func (c Case) String() string {
	switch c {
	case Case(pb.Case_CASE_NOMINATIVE):
		return "nominative"
	case Case(pb.Case_CASE_VOCATIVE):
		return "vocative"
	case Case(pb.Case_CASE_ACCUSATIVE):
		return "accusative"
	case Case(pb.Case_CASE_GENITIVE):
		return "genitive"
	case Case(pb.Case_CASE_DATIVE):
		return "dative"
	case Case(pb.Case_CASE_ABLATIVE):
		return "ablative"
	default:
		return "unknown"
	}
}

func (n Number) String() string {
	switch n {
	case Number(pb.Number_NUMBER_SINGULAR):
		return "singular"
	case Number(pb.Number_NUMBER_PLURAL):
		return "plural"
	default:
		return "unknown"
	}
}

func (g Gender) String() string {
	switch g {
	case Gender(pb.Gender_GENDER_MASCULINE):
		return "masculine"
	case Gender(pb.Gender_GENDER_FEMININE):
		return "feminine"
	case Gender(pb.Gender_GENDER_NEUTER):
		return "neuter"
	default:
		return "unknown"
	}
}

func (t Tense) String() string {
	switch t {
	case Tense(pb.Tense_TENSE_PRESENT):
		return "present"
	case Tense(pb.Tense_TENSE_IMPERFECT):
		return "imperfect"
	case Tense(pb.Tense_TENSE_FUTURE):
		return "future"
	case Tense(pb.Tense_TENSE_PERFECT):
		return "perfect"
	case Tense(pb.Tense_TENSE_PLUPERFECT):
		return "pluperfect"
	case Tense(pb.Tense_TENSE_FUTURE_PERFECT):
		return "future perfect"
	default:
		return "unknown"
	}
}

func (v Voice) String() string {
	switch v {
	case Voice(pb.Voice_VOICE_ACTIVE):
		return "active"
	case Voice(pb.Voice_VOICE_PASSIVE):
		return "passive"
	case Voice(pb.Voice_VOICE_DEPONENT):
		return "deponent"
	case Voice(pb.Voice_VOICE_SEMI_DEPONENT):
		return "semi-deponent"
	default:
		return "unknown"
	}
}

func (m Mood) String() string {
	switch m {
	case Mood(pb.Mood_MOOD_INDICATIVE):
		return "indicative"
	case Mood(pb.Mood_MOOD_SUBJUNCTIVE):
		return "subjunctive"
	case Mood(pb.Mood_MOOD_IMPERATIVE):
		return "imperative"
	case Mood(pb.Mood_MOOD_INFINITIVE):
		return "infinitive"
	case Mood(pb.Mood_MOOD_PARTICIPLE):
		return "participle"
	case Mood(pb.Mood_MOOD_GERUND):
		return "gerund"
	case Mood(pb.Mood_MOOD_SUPINE):
		return "supine"
	default:
		return "unknown"
	}
}

func (p Person) String() string {
	switch p {
	case Person(pb.Person_PERSON_FIRST):
		return "1st person"
	case Person(pb.Person_PERSON_SECOND):
		return "2nd person"
	case Person(pb.Person_PERSON_THIRD):
		return "3rd person"
	default:
		return "unknown"
	}
}

func (d Degree) String() string {
	switch d {
	case Degree(pb.Degree_DEGREE_POSITIVE):
		return "positive"
	case Degree(pb.Degree_DEGREE_COMPARATIVE):
		return "comparative"
	case Degree(pb.Degree_DEGREE_SUPERLATIVE):
		return "superlative"
	default:
		return "unknown"
	}
}
