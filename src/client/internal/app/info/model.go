package info

type Model struct {
	// Layout state

	width, height int

	// Application state

	focused bool
}

func New() *Model {
	return &Model{}
}

func (m *Model) Focus() {
	m.focused = true
}

func (m *Model) Blur() {
	m.focused = false
}

func (m *Model) Focused() bool {
	return m.focused
}
