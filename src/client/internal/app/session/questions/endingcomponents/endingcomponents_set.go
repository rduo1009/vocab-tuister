package endingcomponents

type ComponentSetter interface {
	SetComponent(*EndingComponents)
}

func (c Case) SetComponent(e *EndingComponents) {
	e.Case = c
}

func (n Number) SetComponent(e *EndingComponents) {
	e.Number = n
}

func (g Gender) SetComponent(e *EndingComponents) {
	e.Gender = g
}

func (t Tense) SetComponent(e *EndingComponents) {
	e.Tense = t
}

func (v Voice) SetComponent(e *EndingComponents) {
	e.Voice = v
}

func (m Mood) SetComponent(e *EndingComponents) {
	e.Mood = m
}

func (p Person) SetComponent(e *EndingComponents) {
	e.Person = p
}

func (d Degree) SetComponent(e *EndingComponents) {
	e.Degree = d
}
