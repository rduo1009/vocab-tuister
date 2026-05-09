package endingcomponents

import (
	pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"
)

type ComponentSetter interface {
	SetComponent(*EndingComponents)
}

func (c Case) SetComponent(e *EndingComponents) {
	e.Case = pb.Case(c)
}

func (n Number) SetComponent(e *EndingComponents) {
	e.Number = pb.Number(n)
}

func (g Gender) SetComponent(e *EndingComponents) {
	e.Gender = pb.Gender(g)
}

func (t Tense) SetComponent(e *EndingComponents) {
	e.Tense = pb.Tense(t)
}

func (v Voice) SetComponent(e *EndingComponents) {
	e.Voice = pb.Voice(v)
}

func (m Mood) SetComponent(e *EndingComponents) {
	e.Mood = pb.Mood(m)
}

func (p Person) SetComponent(e *EndingComponents) {
	e.Person = pb.Person(p)
}

func (d Degree) SetComponent(e *EndingComponents) {
	e.Degree = pb.Degree(d)
}
