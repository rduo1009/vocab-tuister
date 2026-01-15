// Package vimtea provides a Vim-like text editor component for terminal applications
package vimtea

// Cursor represents a position in the text buffer with row and column coordinates.
type Cursor struct {
	Row int // Zero-based line index
	Col int // Zero-based column index
}

// Clone creates a copy of the cursor.
func (c Cursor) Clone() Cursor {
	return Cursor{Row: c.Row, Col: c.Col}
}

// newCursor creates a new cursor at the specified position.
func newCursor(row, col int) Cursor {
	return Cursor{Row: row, Col: col}
}

// ensureCursorVisible scrolls the viewport to make sure the cursor is visible
// This is called whenever the cursor moves or the window is resized.
func (m *editorModel) ensureCursorVisible() {
	// If cursor is above the viewport, scroll up
	if m.cursor.Row < m.viewport.YOffset() {
		m.viewport.SetYOffset(m.cursor.Row)
	} else if m.cursor.Row >= m.viewport.YOffset()+m.height {
		// If cursor is below the viewport, scroll down
		m.viewport.SetYOffset(m.cursor.Row - m.height + 1)
	}

	// Ensure cursor is within valid bounds
	m.adjustCursorPosition()
}

// adjustCursorPosition ensures the cursor stays within valid bounds
// Has different behavior based on the current mode (Insert vs Normal/Visual).
func (m *editorModel) adjustCursorPosition() {
	// Keep cursor within valid rows
	if m.cursor.Row < 0 {
		m.cursor.Row = 0
	}
	if m.cursor.Row >= m.buffer.lineCount() {
		m.cursor.Row = m.buffer.lineCount() - 1
	}

	// Adjust column position based on mode
	lineLen := m.buffer.lineLength(m.cursor.Row)
	if m.mode == ModeInsert {
		// In insert mode, cursor can be at end of line
		if m.cursor.Col > lineLen {
			m.cursor.Col = lineLen
		}
	} else {
		// In normal/visual mode, cursor can't be at end of line (except empty lines)
		if lineLen == 0 {
			m.cursor.Col = 0
		} else if m.cursor.Col >= lineLen {
			m.cursor.Col = lineLen - 1
		}
	}

	// Keep cursor within valid columns
	if m.cursor.Col < 0 {
		m.cursor.Col = 0
	}
}
