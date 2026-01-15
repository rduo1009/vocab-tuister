// Package vimtea provides a Vim-like text editor component for terminal applications
package vimtea

import tea "github.com/charmbracelet/bubbletea/v2"

// wrappedBuffer adapts the internal buffer implementation to the Buffer interface
// This wrapping pattern allows the editor model to expose a buffer interface
// without exposing its internal state directly.
type wrappedBuffer struct {
	m *editorModel // Reference to the parent editor model
}

// Text returns the entire buffer content as a string.
func (w *wrappedBuffer) Text() string {
	return w.m.buffer.text()
}

// Lines returns all lines in the buffer as a string slice.
func (w *wrappedBuffer) Lines() []string {
	return w.m.buffer.lines
}

// LineCount returns the number of lines in the buffer.
func (w *wrappedBuffer) LineCount() int {
	return w.m.buffer.lineCount()
}

// LineLength returns the length of the line at the given row.
func (w *wrappedBuffer) LineLength(row int) int {
	return w.m.buffer.lineLength(row)
}

// VisualLineLength returns the visual length of the line at the given row
// This accounts for tabs which visually occupy multiple spaces.
func (w *wrappedBuffer) VisualLineLength(row int) int {
	return w.m.buffer.visualLineLength(row)
}

// InsertAt inserts text at the specified position.
func (w *wrappedBuffer) InsertAt(row, col int, text string) {
	w.m.buffer.saveUndoState(w.m.cursor)
	w.m.buffer.insertAt(row, col, text)
}

// DeleteAt deletes text between the specified positions.
func (w *wrappedBuffer) DeleteAt(startRow, startCol, endRow, endCol int) {
	w.m.buffer.saveUndoState(w.m.cursor)
	w.m.buffer.deleteAt(startRow, startCol, endRow, endCol)
}

// Undo reverts the last change and returns a command with the new cursor position.
func (w *wrappedBuffer) Undo() tea.Cmd {
	return w.m.buffer.undo(w.m.cursor)
}

// Redo reapplies a previously undone change.
func (w *wrappedBuffer) Redo() tea.Cmd {
	return w.m.buffer.redo(w.m.cursor)
}

// CanUndo returns whether there are changes that can be undone.
func (w *wrappedBuffer) CanUndo() bool {
	return w.m.buffer.canUndo()
}

// CanRedo returns whether there are changes that can be redone.
func (w *wrappedBuffer) CanRedo() bool {
	return w.m.buffer.canRedo()
}

// Clear removes all content from the buffer and resets to empty state.
func (w *wrappedBuffer) Clear() tea.Cmd {
	w.m.buffer.saveUndoState(w.m.cursor)
	w.m.buffer.clear()
	w.m.cursor = newCursor(0, 0)
	return func() tea.Msg {
		return nil
	}
}
