package settings

import (
	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
)

type Model struct {
	// Layout state

	width, height int

	// Application state

	styles  *styles.StylesWrapper
	focused bool
}

func New(styles *styles.StylesWrapper) *Model {
	return &Model{styles: styles}
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
