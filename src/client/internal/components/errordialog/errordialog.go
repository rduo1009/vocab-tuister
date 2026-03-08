package errordialog

import (
	"math"
	"strings"
	"time"

	"charm.land/bubbles/v2/viewport"
	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"
)

type TimeoutMsg struct{}

type Model struct {
	err             error
	viewport        viewport.Model
	visible         bool
	width           int
	height          int
	lastInteraction time.Time
}

func New() Model {
	return Model{
		viewport: viewport.New(),
		visible:  false,
	}
}

func (m Model) Init() tea.Cmd {
	return nil
}

func (m Model) Update(msg tea.Msg) (Model, tea.Cmd) {
	var (
		cmd  tea.Cmd
		cmds []tea.Cmd
	)

	switch msg := msg.(type) {
	case TimeoutMsg:
		if m.visible {
			// If user interacted recently (within last 3 seconds), restart timer
			if time.Since(m.lastInteraction) < 3*time.Second {
				return m, tea.Tick(3*time.Second, func(t time.Time) tea.Msg {
					return TimeoutMsg{}
				})
			}

			m.visible = false
		}

	case tea.KeyMsg, tea.MouseMsg:
		if m.visible {
			m.lastInteraction = time.Now()
			m.viewport, cmd = m.viewport.Update(msg)
			cmds = append(cmds, cmd)
		}
	}

	return m, tea.Batch(cmds...)
}

func (m *Model) SetError(err error) tea.Cmd {
	m.err = err
	m.visible = true
	m.lastInteraction = time.Now() // Reset interaction timer on new error

	// Set content relative to width
	m.updateViewportContent()

	return tea.Tick(5*time.Second, func(t time.Time) tea.Msg {
		return TimeoutMsg{}
	})
}

func (m *Model) SetWidth(w int) {
	m.width = w / 4
	// Account for border (2) + scrollbar (1)
	m.viewport.SetWidth(m.width - 3)
	m.updateViewportContent()
}

func (m *Model) SetHeight(h int) {
	m.height = h / 4
	// Account for border (2) + header (2) + footer (1 or 0)
	// We'll reserve space for footer just in case, or make it dynamic.
	// Let's reserve 1 line for footer if needed.
	// Actually, calculating dynamic height for viewport in View() is tricky if we want fixed outer height.
	// Let's assume header is 2 lines (border+text), footer is 1 line.
	// Height available for viewport = Height - 2 (Border) - 2 (Header) - 1 (Footer) = Height - 5
	m.viewport.SetHeight(m.height - 5)
}

func (m Model) Visible() bool {
	return m.visible
}

func (m Model) View() string {
	if !m.visible {
		return ""
	}

	borderColor := lipgloss.Color("196")

	dialogStyle := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(borderColor).
		Width(m.width).
		Height(m.height)

	headerStyle := lipgloss.NewStyle().
		Foreground(borderColor).
		Bold(true).
		Padding(0, 1).
		Border(lipgloss.NormalBorder(), false, false, true, false).
		BorderForeground(borderColor).
		Width(m.width - 2)

	header := headerStyle.Render("ⓧ Error")

	viewportView := m.viewport.View()

	// Add scrollbar if needed
	if m.viewport.TotalLineCount() > m.viewport.VisibleLineCount() {
		scrollbar := scrollbar(
			m.viewport.Height(),
			m.viewport.TotalLineCount(),
			m.viewport.VisibleLineCount(),
			m.viewport.YOffset(),
		)
		viewportView = lipgloss.JoinHorizontal(lipgloss.Top, viewportView, scrollbar)
	} else {
		// Padding if no scrollbar to keep alignment consistent if we want,
		// but since we reduced width by 1 for scrollbar generally, we might want to just fill with space?
		// or just let it be. styling choice.
		// For consistency with SetWidth - 3, let's add a space column.
		spacer := strings.TrimRight(strings.Repeat(" \n", m.viewport.Height()), "\n")
		viewportView = lipgloss.JoinHorizontal(lipgloss.Top, viewportView, spacer)
	}

	content := lipgloss.JoinVertical(lipgloss.Left, header, viewportView)

	return dialogStyle.Render(content)
}

func (m *Model) updateViewportContent() {
	if m.err != nil {
		style := lipgloss.NewStyle().
			Width(m.viewport.Width()).
			Foreground(lipgloss.Color("196")) // Red text
		m.viewport.SetContent(style.Render(m.err.Error()))
	}
}

func scrollbar(height, total, visible, offset int) string {
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

	trackStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("240"))
	thumbStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("250"))

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
