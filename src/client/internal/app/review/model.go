package review

type Model struct {
	// Layout state
	width, height int

	// Application state
	focused bool
}

func New() *Model {
	return &Model{}
}

func (m *Model) SetFocused(focused bool) {
	m.focused = focused
}

func (m *Model) Focused() bool {
	return m.focused
}

func (m *Model) ID() string {
	return "ReviewSection"
}
