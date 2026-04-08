package list

import (
	"github.com/alecthomas/chroma/v2"
	"github.com/alecthomas/chroma/v2/lexers"
)

// VocabFile is a Chroma lexer for the vocab-tuister list format.
//
// Tokens mapping (what styles you can map later):
//   - chroma.GenericHeading   -> lines that start with '@' (section headers)
//   - chroma.Comment          -> lines that start with '#'
//   - chroma.GenericStrong    -> the "label" before the ':' (including slashes)
//   - chroma.Punctuation      -> ':' and ',' and other small separators
//   - chroma.CommentPreproc   -> parenthetical metadata like "(f)" "(3-2)" "(212)"
//   - chroma.Name             -> words (English or Latin forms, possibly containing '/')
//   - chroma.Text             -> whitespace or generic remainder
var VocabFile = chroma.MustNewLexer(
	&chroma.Config{
		Name:      "VocabFile",
		Aliases:   []string{"vocab", "vocabfile"},
		MimeTypes: []string{"text/x-vocabfile"},
	},
	func() chroma.Rules {
		return chroma.Rules{
			"root": {
				// Section header: entire line starts with '@'
				{Pattern: `(?m)^@\s*.*$`, Type: chroma.GenericHeading, Mutator: nil},

				// Full-line comment
				{Pattern: `(?m)^\s*#.*$`, Type: chroma.Comment, Mutator: nil},

				// Blank line / whitespace-only
				{Pattern: `(?m)^[ \t]*$`, Type: chroma.Text, Mutator: nil},

				// Label before colon (start of line). We capture the left portion and the colon
				// so the left side can be emphasised (GenericStrong) and the colon is punctuation.
				// The pattern intentionally *stops* at the first colon on the line.
				{
					Pattern: `(?m)^([^\n:]+)(:)`,
					Type:    chroma.ByGroups(chroma.GenericStrong, chroma.Punctuation),
					Mutator: nil,
				},

				// Parenthetical metadata, e.g. (f), (3-2), (212)
				{Pattern: `\([^)]+\)`, Type: chroma.CommentPreproc, Mutator: nil},

				// Comma separators and other small punctuation
				{Pattern: `,`, Type: chroma.Punctuation, Mutator: nil},

				// Words that may contain slashes (e.g. "think/consider", "simulac/simulatque", or multiword with no colon)
				// Allow letters, hyphen, apostrophe, slash; also allow multiword tokens if they don't have punctuation
				{Pattern: `[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'/-]*`, Type: chroma.Name, Mutator: nil},

				// Any remaining whitespace
				{Pattern: `\s+`, Type: chroma.Text, Mutator: nil},

				// Fallback: single character as text
				{Pattern: `.`, Type: chroma.Text, Mutator: nil},
			},
		}
	},
)

func init() {
	lexers.Register(VocabFile)
}
