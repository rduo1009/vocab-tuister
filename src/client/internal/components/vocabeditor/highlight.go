// Package vimtea provides a Vim-like text editor component for terminal applications
package vimtea

import (
	"bytes"
	"strings"
	"time"

	"github.com/alecthomas/chroma/v2/lexers"
	"github.com/alecthomas/chroma/v2/quick"
)

// syntaxHighlighter provides syntax highlighting functionality for the editor
// using the Chroma library for language detection and highlighting.
type syntaxHighlighter struct {
	filename    string            // File name used to determine language
	language    string            // Detected language
	syntaxTheme string            // Chroma theme to use for highlighting
	enabled     bool              // Whether highlighting is enabled
	cache       map[string]string // Cache of highlighted lines for performance
}

// yankHighlight provides visual feedback for yanked (copied) text
// by temporarily highlighting the yanked region.
type yankHighlight struct {
	Active     bool          // Whether the highlight is currently active
	Start      Cursor        // Start position of highlighted region
	End        Cursor        // End position of highlighted region
	StartTime  time.Time     // When the highlight was activated
	Duration   time.Duration // How long the highlight should remain visible
	IsLinewise bool          // Whether this is a line-wise operation
}

// newSyntaxHighlighter creates a new syntax highlighter with the specified theme and filename
// The filename is used to determine the language for syntax highlighting.
func newSyntaxHighlighter(syntaxTheme, fileName string) *syntaxHighlighter {
	return &syntaxHighlighter{
		syntaxTheme: syntaxTheme,
		enabled:     true,
		filename:    fileName,
		cache:       make(map[string]string),
	}
}

// newYankHighlight creates a new inactive yank highlight
// with a default duration of 100ms.
func newYankHighlight() yankHighlight {
	return yankHighlight{
		Active:   false,
		Duration: time.Millisecond * 100,
	}
}

// HighlightLine applies syntax highlighting to a single line of text
// It uses caching to improve performance for repeated lines.
func (sh *syntaxHighlighter) HighlightLine(line string) string {
	// Skip highlighting if disabled or no filename is set
	if !sh.enabled || sh.filename == "" {
		return line
	}

	// Check cache for already highlighted lines
	cacheKey := line
	if cached, ok := sh.cache[cacheKey]; ok {
		return cached
	}

	// Skip empty lines
	if len(line) == 0 {
		return line
	}

	lexer := lexers.Match(sh.filename)

	if lexer == nil {
		return line
	}

	// Apply syntax highlighting
	buf := new(bytes.Buffer)
	err := quick.Highlight(buf, line, lexer.Config().Name, "terminal16m", sh.syntaxTheme)
	if err != nil {
		return line
	}

	// Clean up the result by removing newlines
	highlighted := strings.ReplaceAll(buf.String(), "\n", "")

	// Cache the result for future use
	sh.cache[cacheKey] = highlighted

	return highlighted
}
