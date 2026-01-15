// Package vimtea provides a Vim-like text editor component for terminal applications
package vimtea

import (
	"fmt"
	"regexp"
	"strings"
	"unicode/utf8"

	"github.com/charmbracelet/lipgloss/v2"
)

// Regular expression for matching ANSI escape sequences
// Used to correctly calculate visible text length with syntax highlighting.
var ansiRegex = regexp.MustCompile(`\x1b\[[0-9;]*[a-zA-Z]`)

// renderTab renders a tab character with visual representation using spaces.
func renderTab(col int) string {
	spaces := tabWidth - (col % tabWidth)
	return strings.Repeat(" ", spaces)
}

// visualLength calculates the visual length of a string, counting tabs as tabWidth spaces.
func visualLength(s string, startCol int) int {
	length := 0
	for _, r := range s {
		if r == '\t' {
			// Tab advances to the next tab stop
			spaces := tabWidth - ((startCol + length) % tabWidth)
			length += spaces
		} else {
			length++
		}
	}
	return length
}

// bufferToVisualPosition converts a buffer position to a visual position
// This accounts for tabs that visually occupy multiple columns.
func bufferToVisualPosition(line string, bufferCol int) int {
	if bufferCol > len(line) {
		bufferCol = len(line)
	}

	visualCol := 0
	for i, r := range line {
		if i >= bufferCol {
			break
		}

		if r == '\t' {
			spaces := tabWidth - (visualCol % tabWidth)
			visualCol += spaces
		} else {
			visualCol++
		}
	}
	return visualCol
}

// renderLineWithTabs renders a line with proper tab expansion.
func renderLineWithTabs(line string) string {
	var sb strings.Builder
	visualCol := 0

	for _, r := range line {
		if r == '\t' {
			spaces := tabWidth - (visualCol % tabWidth)
			sb.WriteString(strings.Repeat(" ", spaces))
			visualCol += spaces
		} else {
			sb.WriteRune(r)
			visualCol++
		}
	}

	return sb.String()
}

// View renders the editor and returns it as a string
// This is part of the bubbletea.Model interface.
func (m *editorModel) View() string {
	// Build components from top to bottom
	components := []string{
		m.renderContent(), // Main editor content
	}
	if m.enableStatusBar {
		components = append(components, m.renderStatusLine()) // Status bar and command line
	}

	// Join all components vertically
	return lipgloss.JoinVertical(
		lipgloss.Top,
		components...,
	)
}

func (m *editorModel) renderContent() string {
	var sb strings.Builder

	var selStart, selEnd Cursor
	if m.mode == ModeVisual {
		selStart, selEnd = m.GetSelectionBoundary()
	}

	visibleContent := m.getVisibleContent()

	for i, line := range visibleContent {
		lineNum := i + m.viewport.YOffset() + 1
		rowIdx := lineNum - 1

		sb.WriteString(m.renderLineNumber(lineNum, rowIdx))

		if rowIdx >= m.buffer.lineCount() {
			sb.WriteString("\n")
			continue
		}

		inVisualSelection := m.mode == ModeVisual && rowIdx >= selStart.Row && rowIdx <= selEnd.Row
		sb.WriteString(m.renderLine(line, rowIdx, inVisualSelection, selStart, selEnd))
		sb.WriteString("\n")
	}

	return sb.String()
}

func (m *editorModel) renderLine(line string, rowIdx int, inVisualSelection bool, selStart, selEnd Cursor) string {
	displayLine := renderLineWithTabs(line)

	if m.mode == ModeVisual && m.isVisualLine && inVisualSelection {
		return m.selectedStyle.Render(displayLine)
	}

	if m.mode != ModeVisual && m.yankHighlight.Active && m.isLineInYankHighlight(rowIdx) {
		return m.renderLineWithYankHighlight(line, rowIdx)
	}

	var highlightedLine string
	if m.highlighter != nil && m.highlighter.enabled {
		highlightedLine = m.highlighter.HighlightLine(displayLine)
	} else {
		highlightedLine = displayLine
	}

	if rowIdx == m.cursor.Row {
		if len(line) == 0 {
			if m.cursor.Col == 0 {
				return m.renderCursor(" ")
			}
			return ""
		}

		if m.cursor.Col >= len(line) {
			return highlightedLine + m.renderCursor(" ")
		}

		if m.mode == ModeVisual && !m.isVisualLine && inVisualSelection {
			return m.renderLineWithCursorInVisualSelection(line, rowIdx, selStart, selEnd)
		}

		if m.highlighter != nil && m.highlighter.enabled && displayLine != highlightedLine {
			return m.renderSyntaxHighlightedCursorLine(highlightedLine, line)
		}

		return m.renderRegularCursorLine(line)
	}

	if m.mode == ModeVisual && !m.isVisualLine && inVisualSelection {
		return m.renderLineInVisualSelection(line, rowIdx, selStart, selEnd)
	}

	return highlightedLine
}

func (m *editorModel) renderCursor(char string) string {
	if !m.cursorBlink {
		return char
	}

	switch m.mode {
	case ModeInsert:
		return lipgloss.NewStyle().Underline(true).Render(char)
	case ModeCommand:
		return char
	default:
		return m.cursorStyle.Render(char)
	}
}

func (m *editorModel) renderLineNumber(lineNum, rowIdx int) string {
	if rowIdx >= m.buffer.lineCount() {
		return m.lineNumberStyle.Render("    ")
	}

	if rowIdx == m.cursor.Row {
		return m.currentLineNumberStyle.Render(fmt.Sprintf("%4d", lineNum))
	}

	if m.relativeNumbers {
		distance := abs(rowIdx - m.cursor.Row)
		return m.lineNumberStyle.Render(fmt.Sprintf("%4d", distance))
	}

	return m.lineNumberStyle.Render(fmt.Sprintf("%4d", lineNum))
}

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func (m *editorModel) renderRegularCursorLine(line string) string {
	var sb strings.Builder
	visualCol := 0

	// Process characters up to the cursor position
	for i, r := range line {
		if i >= m.cursor.Col {
			break
		}

		if r == '\t' {
			spaces := tabWidth - (visualCol % tabWidth)
			sb.WriteString(strings.Repeat(" ", spaces))
			visualCol += spaces
		} else {
			sb.WriteRune(r)
			visualCol++
		}
	}

	// Handle cursor character
	if m.cursor.Col < len(line) {
		cursorRune, _ := utf8.DecodeRuneInString(line[m.cursor.Col:])
		if cursorRune == '\t' {
			// For tab, just highlight the first space
			sb.WriteString(m.renderCursor(" "))

			// Write the remaining spaces
			spaces := tabWidth - 1 - (visualCol % tabWidth)
			if spaces > 0 {
				sb.WriteString(strings.Repeat(" ", spaces))
			}
			visualCol += tabWidth - (visualCol % tabWidth)
		} else {
			sb.WriteString(m.renderCursor(string(cursorRune)))
			visualCol++
		}
	} else {
		// Cursor at end of line
		sb.WriteString(m.renderCursor(" "))
		visualCol++
	}

	// Process remaining characters after cursor
	if m.cursor.Col < len(line)-1 {
		for _, r := range line[m.cursor.Col+1:] {
			if r == '\t' {
				spaces := tabWidth - (visualCol % tabWidth)
				sb.WriteString(strings.Repeat(" ", spaces))
				visualCol += spaces
			} else {
				sb.WriteRune(r)
				visualCol++
			}
		}
	}

	return sb.String()
}

func (m *editorModel) renderSyntaxHighlightedCursorLine(highlightedLine, plainLine string) string {
	// For syntax highlighting with tabs, we need to:
	// 1. Render the plain line with proper tab expansion
	// 2. Apply cursor highlighting at the correct position

	// If the cursor is at the end, just append it
	if m.cursor.Col >= len(plainLine) {
		return highlightedLine + m.renderCursor(" ")
	}

	// Calculate the visual position of the cursor
	visualCursorPos := bufferToVisualPosition(plainLine, m.cursor.Col)

	// Get the character at the cursor position
	var cursorChar string
	if m.cursor.Col < len(plainLine) {
		if plainLine[m.cursor.Col] == '\t' {
			cursorChar = " " // Show first space of tab
		} else {
			cursorChar = string(plainLine[m.cursor.Col])
		}
	} else {
		cursorChar = " "
	}

	// If we're dealing with a tab at cursor position, we need special handling
	if m.cursor.Col < len(plainLine) && plainLine[m.cursor.Col] == '\t' {
		return m.renderRegularCursorLine(plainLine)
	}

	// For non-tab characters, we can try to locate the cursor position in the highlighted line
	// Find all ANSI escape sequences in the highlighted line
	ansiMatches := ansiRegex.FindAllStringIndex(highlightedLine, -1)

	// Match the visual position in the highlighted line
	visibleIdx := 0
	cursorHighlightPos := -1

	for i := 0; i < len(highlightedLine); {
		isAnsi := false
		for _, match := range ansiMatches {
			if match[0] == i {
				i = match[1]
				isAnsi = true
				break
			}
		}

		if isAnsi {
			continue
		}

		if visibleIdx == visualCursorPos {
			cursorHighlightPos = i
			break
		}

		visibleIdx++
		i++
	}

	// If we couldn't find the cursor position in the highlighted output,
	// fall back to regular cursor line rendering
	if cursorHighlightPos == -1 {
		return m.renderRegularCursorLine(plainLine)
	}

	// Extract ANSI codes that should be active before the cursor
	var ansiBeforeCursor string
	for _, match := range ansiMatches {
		if match[0] < cursorHighlightPos {
			ansiBeforeCursor += highlightedLine[match[0]:match[1]]
		}
	}

	// Build the final output with the cursor properly highlighted
	var sb strings.Builder
	sb.WriteString(highlightedLine[:cursorHighlightPos])
	sb.WriteString("\x1b[0m") // Reset all ANSI formatting

	sb.WriteString(m.renderCursor(cursorChar))

	// Restore ANSI formatting for text after the cursor
	sb.WriteString(ansiBeforeCursor)

	if cursorHighlightPos+1 < len(highlightedLine) {
		afterCursorStart := cursorHighlightPos + 1

		// Skip any ANSI sequences immediately after the cursor
		for _, match := range ansiMatches {
			if afterCursorStart >= match[0] && afterCursorStart < match[1] {
				afterCursorStart = match[1]
				break
			}
		}

		sb.WriteString(highlightedLine[afterCursorStart:])
	}

	return sb.String()
}

func (m *editorModel) renderLineWithCursorInVisualSelection(line string, rowIdx int, selStart, selEnd Cursor) string {
	var sb strings.Builder

	// Get selection boundaries in buffer coordinates
	selBegin := 0
	if rowIdx == selStart.Row {
		selBegin = selStart.Col
	}

	selEndCol := len(line)
	if rowIdx == selEnd.Row {
		selEndCol = selEnd.Col + 1
	}

	// First, expand tabs to get the display line
	displayLine := renderLineWithTabs(line)

	// Apply syntax highlighting if enabled
	var highlightedLine string
	if m.highlighter != nil && m.highlighter.enabled {
		highlightedLine = m.highlighter.HighlightLine(displayLine)
	} else {
		highlightedLine = displayLine
	}

	// If we're dealing with just plain text without highlighting, use the original rendering method
	if highlightedLine == displayLine {
		return m.renderLineWithCursorInVisualSelectionPlain(line, rowIdx, selStart, selEnd)
	}

	// When we have syntax highlighting, we need to modify our approach
	// Extract ANSI escape sequences in the highlighted text
	ansiMatches := ansiRegex.FindAllStringIndex(highlightedLine, -1)

	// Calculate visual positions and create a mapping from visual position to highlighted text index
	visToHighlightIndex := make(map[int]int)
	visibleIdx := 0

	for i := 0; i < len(highlightedLine); {
		isAnsi := false
		for _, match := range ansiMatches {
			if match[0] == i {
				i = match[1]
				isAnsi = true
				break
			}
		}

		if isAnsi {
			continue
		}

		visToHighlightIndex[visibleIdx] = i
		visibleIdx++
		i++
	}

	// Convert buffer positions to visual positions
	visSelBegin := bufferToVisualPosition(line, selBegin)
	visSelEnd := bufferToVisualPosition(line, selEndCol)
	visCursorPos := bufferToVisualPosition(line, m.cursor.Col)

	// Now render with proper selection and cursor highlighting
	visPos := 0
	inSelection := false
	ansiStyling := "\x1b[0m" // Start with reset

	// Process highlighting while preserving ANSI codes
	for i := 0; i < len(highlightedLine); {
		// Check if we're at an ANSI sequence
		isAnsi := false
		for _, match := range ansiMatches {
			if match[0] == i {
				ansiStyling = highlightedLine[match[0]:match[1]]
				i = match[1]
				isAnsi = true
				break
			}
		}

		if isAnsi {
			continue
		}

		// Visual position transitions
		if visPos == visSelBegin {
			inSelection = true
		}

		if visPos == visSelEnd {
			inSelection = false
		}

		// Get current character
		char := string(highlightedLine[i])

		// Handle cursor character with priority
		if visPos == visCursorPos {
			if m.cursorBlink {
				sb.WriteString("\x1b[0m") // Reset all formatting
				sb.WriteString(m.cursorStyle.Render(char))
				sb.WriteString("\x1b[0m") // Reset again
			} else {
				sb.WriteString("\x1b[0m") // Reset all formatting
				sb.WriteString(m.selectedStyle.Render(char))
				sb.WriteString("\x1b[0m") // Reset again
			}
		} else if inSelection {
			// In selection but not at cursor
			sb.WriteString("\x1b[0m") // Reset all formatting
			sb.WriteString(m.selectedStyle.Render(char))
			sb.WriteString("\x1b[0m") // Reset again
		} else {
			// Not in selection, use syntax highlighting
			sb.WriteString(ansiStyling) // Apply current styling
			sb.WriteString(char)
		}

		visPos++
		i++

		// Restore ANSI styling for next character
		if !inSelection && visPos != visCursorPos {
			sb.WriteString(ansiStyling)
		}
	}

	return sb.String()
}

// renderLineWithCursorInVisualSelectionPlain handles rendering a line with a cursor in visual selection
// when no syntax highlighting is applied.
func (m *editorModel) renderLineWithCursorInVisualSelectionPlain(line string, rowIdx int, selStart, selEnd Cursor) string {
	var sb strings.Builder

	// Get selection boundaries in buffer coordinates
	selBegin := 0
	if rowIdx == selStart.Row {
		selBegin = selStart.Col
	}

	selEndCol := len(line)
	if rowIdx == selEnd.Row {
		selEndCol = selEnd.Col + 1
	}

	// Process the line with proper tab rendering
	curVisualPos := 0
	for i, r := range line {
		// Handle character before selection start
		if i < selBegin {
			if r == '\t' {
				spaces := tabWidth - (curVisualPos % tabWidth)
				sb.WriteString(strings.Repeat(" ", spaces))
				curVisualPos += spaces
			} else {
				sb.WriteRune(r)
				curVisualPos++
			}
			continue
		}

		// Handle cursor character
		if i == m.cursor.Col {
			// Get appropriate character display
			var cursorChar string
			if r == '\t' {
				cursorChar = " " // Show first space of tab
			} else {
				cursorChar = string(r)
			}

			if m.cursorBlink {
				sb.WriteString(m.cursorStyle.Render(cursorChar))
			} else {
				sb.WriteString(m.selectedStyle.Render(cursorChar))
			}

			// Handle remaining spaces for tab
			if r == '\t' {
				spaces := tabWidth - 1 - (curVisualPos % tabWidth)
				if spaces > 0 {
					sb.WriteString(m.selectedStyle.Render(strings.Repeat(" ", spaces)))
				}
				curVisualPos += tabWidth - (curVisualPos % tabWidth)
			} else {
				curVisualPos++
			}
			continue
		}

		// Handle selection (non-cursor)
		if i < selEndCol {
			if r == '\t' {
				spaces := tabWidth - (curVisualPos % tabWidth)
				sb.WriteString(m.selectedStyle.Render(strings.Repeat(" ", spaces)))
				curVisualPos += spaces
			} else {
				sb.WriteString(m.selectedStyle.Render(string(r)))
				curVisualPos++
			}
			continue
		}

		// Handle character after selection end
		if r == '\t' {
			spaces := tabWidth - (curVisualPos % tabWidth)
			sb.WriteString(strings.Repeat(" ", spaces))
			curVisualPos += spaces
		} else {
			sb.WriteRune(r)
			curVisualPos++
		}
	}

	return sb.String()
}

func (m *editorModel) renderLineInVisualSelection(line string, rowIdx int, selStart, selEnd Cursor) string {
	var sb strings.Builder

	// Get selection boundaries in buffer coordinates
	selBegin := 0
	if rowIdx == selStart.Row {
		selBegin = selStart.Col
	}

	selEndCol := len(line)
	if rowIdx == selEnd.Row {
		selEndCol = selEnd.Col + 1
	}

	// First, expand tabs to get the display line
	displayLine := renderLineWithTabs(line)

	// Apply syntax highlighting if enabled
	var highlightedLine string
	if m.highlighter != nil && m.highlighter.enabled {
		highlightedLine = m.highlighter.HighlightLine(displayLine)
	} else {
		highlightedLine = displayLine
	}

	// If we're dealing with just plain text without highlighting, use the simplified method
	if highlightedLine == displayLine {
		return m.renderLineInVisualSelectionPlain(line, rowIdx, selStart, selEnd)
	}

	// When we have syntax highlighting, we need to modify our approach
	// Extract ANSI escape sequences in the highlighted text
	ansiMatches := ansiRegex.FindAllStringIndex(highlightedLine, -1)

	// Calculate visual positions and create a mapping from visual position to highlighted text index
	visToHighlightIndex := make(map[int]int)
	visibleIdx := 0

	for i := 0; i < len(highlightedLine); {
		isAnsi := false
		for _, match := range ansiMatches {
			if match[0] == i {
				i = match[1]
				isAnsi = true
				break
			}
		}

		if isAnsi {
			continue
		}

		visToHighlightIndex[visibleIdx] = i
		visibleIdx++
		i++
	}

	// Convert buffer positions to visual positions
	visSelBegin := bufferToVisualPosition(line, selBegin)
	visSelEnd := bufferToVisualPosition(line, selEndCol)

	// Now render with proper selection highlighting
	visPos := 0
	inSelection := false
	ansiStyling := "\x1b[0m" // Start with reset

	// Process highlighting while preserving ANSI codes
	for i := 0; i < len(highlightedLine); {
		// Check if we're at an ANSI sequence
		isAnsi := false
		for _, match := range ansiMatches {
			if match[0] == i {
				ansiStyling = highlightedLine[match[0]:match[1]]
				i = match[1]
				isAnsi = true
				break
			}
		}

		if isAnsi {
			continue
		}

		// Visual position transitions
		if visPos == visSelBegin {
			inSelection = true
		}

		if visPos == visSelEnd {
			inSelection = false
		}

		// Get current character
		char := string(highlightedLine[i])

		if inSelection {
			// In selection
			sb.WriteString("\x1b[0m") // Reset all formatting
			sb.WriteString(m.selectedStyle.Render(char))
			sb.WriteString("\x1b[0m") // Reset again
		} else {
			// Not in selection, use syntax highlighting
			sb.WriteString(ansiStyling) // Apply current styling
			sb.WriteString(char)
		}

		visPos++
		i++

		// Restore ANSI styling for next character
		if !inSelection {
			sb.WriteString(ansiStyling)
		}
	}

	return sb.String()
}

// renderLineInVisualSelectionPlain handles rendering a line in visual selection
// when no syntax highlighting is applied.
func (m *editorModel) renderLineInVisualSelectionPlain(line string, rowIdx int, selStart, selEnd Cursor) string {
	var sb strings.Builder

	// Get selection boundaries in buffer coordinates
	selBegin := 0
	if rowIdx == selStart.Row {
		selBegin = selStart.Col
	}

	selEndCol := len(line)
	if rowIdx == selEnd.Row {
		selEndCol = selEnd.Col + 1
	}

	// Process the line with proper tab rendering
	curVisualPos := 0
	for i, r := range line {
		// Handle character before selection start
		if i < selBegin {
			if r == '\t' {
				spaces := tabWidth - (curVisualPos % tabWidth)
				sb.WriteString(strings.Repeat(" ", spaces))
				curVisualPos += spaces
			} else {
				sb.WriteRune(r)
				curVisualPos++
			}
			continue
		}

		// Handle selection
		if i < selEndCol {
			if r == '\t' {
				spaces := tabWidth - (curVisualPos % tabWidth)
				sb.WriteString(m.selectedStyle.Render(strings.Repeat(" ", spaces)))
				curVisualPos += spaces
			} else {
				sb.WriteString(m.selectedStyle.Render(string(r)))
				curVisualPos++
			}
			continue
		}

		// Handle character after selection end
		if r == '\t' {
			spaces := tabWidth - (curVisualPos % tabWidth)
			sb.WriteString(strings.Repeat(" ", spaces))
			curVisualPos += spaces
		} else {
			sb.WriteRune(r)
			curVisualPos++
		}
	}

	return sb.String()
}

func (m editorModel) getVisibleContent() []string {
	startLine := m.viewport.YOffset()
	endLine := startLine + m.height

	if startLine < 0 {
		startLine = 0
	}

	contentLines := []string{}

	for i := startLine; i < min(endLine, m.buffer.lineCount()); i++ {
		contentLines = append(contentLines, m.buffer.Line(i))
	}

	emptyLinesNeeded := m.height - len(contentLines)
	for range emptyLinesNeeded {
		contentLines = append(contentLines, "")
	}

	return contentLines
}

func (m *editorModel) renderStatusLine() string {
	status := m.getStatusText()
	cursorPos := fmt.Sprintf(" %d:%d ", m.cursor.Row+1, m.cursor.Col+1)

	padding := max(m.width-lipgloss.Width(status)-lipgloss.Width(cursorPos), 0)

	return m.statusStyle.Render(status + strings.Repeat(" ", padding) + cursorPos)
}

func (m *editorModel) getStatusText() string {
	if m.mode == ModeCommand {
		return ":" + m.commandBuffer
	}

	status := fmt.Sprintf(" %s", m.mode)
	if len(m.keySequence) > 0 {
		status += fmt.Sprintf(" | %s", strings.Join(m.keySequence, ""))
	}

	if m.statusMessage != "" {
		status += fmt.Sprintf(" | %s", m.statusMessage)
	}

	return status
}

func (m *editorModel) isLineInYankHighlight(rowIdx int) bool {
	return m.yankHighlight.Active &&
		rowIdx >= m.yankHighlight.Start.Row && rowIdx <= m.yankHighlight.End.Row
}

func (m *editorModel) getYankHighlightBounds(rowIdx int) (int, int) {
	if !m.yankHighlight.Active || !m.isLineInYankHighlight(rowIdx) {
		return -1, -1
	}

	start := 0
	end := m.buffer.lineLength(rowIdx)

	if !m.yankHighlight.IsLinewise {
		if rowIdx == m.yankHighlight.Start.Row {
			start = m.yankHighlight.Start.Col
		}

		if rowIdx == m.yankHighlight.End.Row {
			end = m.yankHighlight.End.Col + 1
		}
	}

	return start, end
}

func (m *editorModel) renderLineWithYankHighlight(line string, rowIdx int) string {
	var sb strings.Builder
	highlightStyle := lipgloss.NewStyle().Background(lipgloss.Color("7"))

	start, end := m.getYankHighlightBounds(rowIdx)
	if start < 0 || end < 0 {
		return renderLineWithTabs(line)
	}

	start = max(0, min(start, len(line)))
	end = max(0, min(end, len(line)))

	// Process the line with proper tab rendering
	curVisualPos := 0
	for i, r := range line {
		// Handle character before highlight start
		if i < start {
			if r == '\t' {
				spaces := tabWidth - (curVisualPos % tabWidth)
				sb.WriteString(strings.Repeat(" ", spaces))
				curVisualPos += spaces
			} else {
				sb.WriteRune(r)
				curVisualPos++
			}
			continue
		}

		// Handle cursor character within highlight
		if i == m.cursor.Col && rowIdx == m.cursor.Row && i >= start && i < end {
			// Get appropriate character display
			var cursorChar string
			if r == '\t' {
				cursorChar = " " // Show first space of tab
			} else {
				cursorChar = string(r)
			}

			if m.cursorBlink {
				sb.WriteString(m.cursorStyle.Render(cursorChar))
			} else {
				sb.WriteString(highlightStyle.Render(cursorChar))
			}

			// Handle remaining spaces for tab
			if r == '\t' {
				spaces := tabWidth - 1 - (curVisualPos % tabWidth)
				if spaces > 0 {
					sb.WriteString(highlightStyle.Render(strings.Repeat(" ", spaces)))
				}
				curVisualPos += tabWidth - (curVisualPos % tabWidth)
			} else {
				curVisualPos++
			}
			continue
		}

		// Handle highlighted character (non-cursor)
		if i < end {
			if r == '\t' {
				spaces := tabWidth - (curVisualPos % tabWidth)
				sb.WriteString(highlightStyle.Render(strings.Repeat(" ", spaces)))
				curVisualPos += spaces
			} else {
				sb.WriteString(highlightStyle.Render(string(r)))
				curVisualPos++
			}
			continue
		}

		// Handle character after highlight end
		if r == '\t' {
			spaces := tabWidth - (curVisualPos % tabWidth)
			sb.WriteString(strings.Repeat(" ", spaces))
			curVisualPos += spaces
		} else {
			sb.WriteRune(r)
			curVisualPos++
		}
	}

	return sb.String()
}
