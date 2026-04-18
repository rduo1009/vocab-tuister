package styles

import (
	"image/color"
	"math"
	"strings"

	"charm.land/lipgloss/v2"
	tint "github.com/lrstanley/bubbletint/v2"
)

type StylesWrapper struct{ Styles }

type Styles struct {
	Title  lipgloss.Style
	Bold   lipgloss.Style
	Italic lipgloss.Style
	Faint  lipgloss.Style
	Error  lipgloss.Style // red text without bolding or italics

	TabBorder     func(active, focused bool, pad int) lipgloss.Style
	TabGap        func(focused bool) lipgloss.Style
	NormalBorder  func(focused bool) lipgloss.Style
	OverlayBorder lipgloss.Style
	Button        func(active, focused bool) lipgloss.Style
	Scrollbar     func(height, total, visible, offset int) string

	LoadSection struct {
		LabelMissing lipgloss.Style
		LabelPending lipgloss.Style
		LabelLoaded  lipgloss.Style
		LabelSep     lipgloss.Style
	}

	SessionPage struct {
		Correct   lipgloss.Style
		Incorrect lipgloss.Style
	}

	MultipleChoice struct {
		Option     func(focused bool, color color.Color) lipgloss.Style
		Unanswered color.Color
		Correct    color.Color
		Incorrect  color.Color
	}

	Dropdown struct {
		Item func(focused bool) lipgloss.Style
	}

	ErrorDialog struct {
		Border lipgloss.Style
		Header lipgloss.Style
	}
}

func DefaultStyles(theme *tint.Tint) Styles {
	s := Styles{}

	s.Title = lipgloss.NewStyle().Bold(true).Underline(true)
	s.Bold = lipgloss.NewStyle().Bold(true)
	s.Italic = lipgloss.NewStyle().Italic(true)
	s.Faint = lipgloss.NewStyle().Faint(true)
	s.Error = lipgloss.NewStyle().Foreground(theme.Red)

	inactiveTabBorder := func() lipgloss.Border {
		b := lipgloss.RoundedBorder()
		b.BottomLeft = "┴"
		b.BottomRight = "┴"
		return b
	}()
	activeTabBorder := func() lipgloss.Border {
		b := lipgloss.RoundedBorder()
		b.Bottom = " "
		b.BottomLeft = "┘"
		b.BottomRight = "└"
		return b
	}()
	s.TabBorder = func(active, focused bool, pad int) lipgloss.Style {
		var style lipgloss.Style
		if active {
			style = style.Border(activeTabBorder, true)
		} else {
			style = style.Border(inactiveTabBorder, true)
		}

		if focused {
			style = style.BorderForeground(theme.Blue)
		} else {
			style = style.BorderForeground(theme.White)
		}

		return style.Padding(0, pad)
	}
	s.TabGap = func(focused bool) lipgloss.Style {
		style := lipgloss.NewStyle().Border(inactiveTabBorder, true)
		if focused {
			style = style.BorderForeground(theme.Blue)
		} else {
			style = style.BorderForeground(theme.White)
		}

		return style.BorderTop(false).
			BorderLeft(false).
			BorderRight(false)
	}

	s.NormalBorder = func(focused bool) lipgloss.Style {
		if focused {
			return lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).BorderForeground(theme.Blue)
		}
		return lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).BorderForeground(theme.White)
	}
	s.OverlayBorder = lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).BorderForeground(theme.Cyan)

	s.Button = func(active, focused bool) lipgloss.Style {
		style := lipgloss.NewStyle().Padding(0, 1)

		if active {
			style = style.Foreground(lipgloss.Color("#fff7db")).
				Background(lipgloss.Color("#888b7e"))
		} else {
			style = style.Foreground(lipgloss.Color("#a9a9a9")).
				Background(lipgloss.Color("#555555"))
		}

		if focused {
			style = style.Italic(true).Underline(true)
		}

		return style
	}

	s.Scrollbar = func(height, total, visible, offset int) string {
		if height == 0 {
			return ""
		}

		if total <= visible {
			return strings.TrimRight(strings.Repeat(" \n", height), "\n")
		}

		ratio := float64(height) / float64(total)
		thumbHeight := int(math.Max(1, math.Round(float64(visible)*ratio)))
		// Bounds check
		thumbOffset := max(0, min(int(math.Round(float64(offset)*ratio)), height-thumbHeight))

		trackStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("#585858"))
		thumbStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("#bcbcbc"))

		trackChar := "│"
		thumbChar := "█"

		track := trackStyle.Render(trackChar)
		thumb := thumbStyle.Render(thumbChar)

		bar := ""

		var barSb185 strings.Builder
		for i := range height {
			if i >= thumbOffset && i < thumbOffset+thumbHeight {
				barSb185.WriteString(thumb + "\n")
			} else {
				barSb185.WriteString(track + "\n")
			}
		}

		bar += barSb185.String()

		return strings.TrimRight(bar, "\n")
	}

	s.LoadSection.LabelMissing = lipgloss.NewStyle().Foreground(theme.Red)
	s.LoadSection.LabelPending = lipgloss.NewStyle().Foreground(theme.Yellow)
	s.LoadSection.LabelLoaded = lipgloss.NewStyle().Foreground(theme.Green)
	s.LoadSection.LabelSep = lipgloss.NewStyle().Foreground(lipgloss.Lighten(theme.Black, 0.1))

	s.SessionPage.Correct = lipgloss.NewStyle().Bold(true).Foreground(theme.Green)
	s.SessionPage.Incorrect = lipgloss.NewStyle().Bold(true).Foreground(theme.Red)

	s.MultipleChoice.Option = func(focused bool, color color.Color) lipgloss.Style {
		borderColor := color
		if focused {
			if color == theme.White {
				borderColor = theme.Purple
			} else {
				borderColor = lipgloss.Lighten(borderColor, 0.1)
			}
		}

		return lipgloss.NewStyle().
			Padding(0, 4).
			MarginBottom(1).
			Border(lipgloss.NormalBorder()).
			BorderForeground(borderColor).
			Align(lipgloss.Left)
	}
	s.MultipleChoice.Unanswered = theme.White
	s.MultipleChoice.Correct = theme.Green
	s.MultipleChoice.Incorrect = theme.Red

	s.Dropdown.Item = func(selected bool) lipgloss.Style {
		if selected {
			return lipgloss.NewStyle().Background(lipgloss.Color("#a7a7a7")).Padding(0, 1)
		}
		return lipgloss.NewStyle().Background(lipgloss.Color("#707070")).Padding(0, 1)
	}

	s.ErrorDialog.Border = lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(theme.Red)
	s.ErrorDialog.Header = lipgloss.NewStyle().
		Foreground(theme.Red).
		Bold(true).
		Padding(0, 1).
		Border(lipgloss.NormalBorder(), false, false, true, false).
		BorderForeground(theme.Red)

	return s
}
