package session

import (
	"fmt"

	"charm.land/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questioncomponents"
)

func (m *Model) SetWidth(width int) {
	m.width = width
}

func (m *Model) SetHeight(height int) {
	m.height = height
}

func (m *Model) HasOverlay() bool {
	return m.dropdownActive
}

func (m *Model) OverlayView(width, height int) (view string, x, y int) {
	if q, ok := m.questions[m.currentIndex].(*questioncomponents.ParseQuestionModel); ok {
		view = q.Dropdowns[m.activeDropdownIndex].View()

		x = 2
		for i := range m.activeDropdownIndex {
			x += q.Dropdowns[i].GetWidth() + 1
		}

		y = 6

		return view, x, y
	}

	panic("unreachable")
}

func (m *Model) View() string {
	var content string
	switch m.appStatus {
	case Unavailable:
		messageView := "List and/or config have not been loaded into server!"

		returnButtonView := m.styles.Button(true, m.returnButton.Focused()).Render("Return to create page")

		content = lipgloss.JoinVertical(lipgloss.Left, messageView, returnButtonView)

		return m.styles.NormalBorder(m.returnButton.Focused()).
			Width(m.width).
			Height(m.height).
			Render(content)

	case Uninitialised:
		content = "Loading..."

		// probs doesn't matter
		return m.styles.NormalBorder(false).
			Width(m.width).
			Height(m.height).
			Render(content)

	case Initialised:
		titleView := m.styles.Title.Render(fmt.Sprintf("Question %d/%d", m.currentIndex+1, m.questionCount))

		var footerView string
		if m.answeredCount == 0 {
			footerView = "Score: 0/0 (0%)"
		} else {
			footerView = fmt.Sprintf(
				"Score: %d/%d (%.0f%%)",
				m.correctCount,
				m.answeredCount,
				100*float64(m.correctCount)/float64(m.answeredCount),
			)
		}
		footerView = m.styles.Text.Render(footerView)

		m.questions[m.currentIndex].SetWidth(m.width - 2)
		m.questions[m.currentIndex].SetHeight(
			m.height - lipgloss.Height(titleView) - lipgloss.Height(footerView) - 2,
		)
		inputView := m.questions[m.currentIndex].View()

		content = lipgloss.JoinVertical(lipgloss.Left, titleView, inputView, footerView)

		return m.styles.NormalBorder(m.questions[m.currentIndex].Focused()).
			Width(m.width).
			Height(m.height).
			Render(content)

	case Completed:
		messageView := "Session completed!"

		scoreView := fmt.Sprintf(
			"Score: %d/%d (%.0f%%)",
			m.correctCount,
			m.answeredCount,
			100*float64(m.correctCount)/float64(m.answeredCount),
		)

		returnButtonView := m.styles.Button(true, m.returnButton.Focused()).
			MarginRight(2).
			Render("Return to create page")
		restartButtonView := m.styles.Button(true, m.restartButton.Focused()).Render("Try again")
		buttonView := lipgloss.JoinHorizontal(lipgloss.Top, returnButtonView, restartButtonView)

		content = lipgloss.JoinVertical(lipgloss.Left, messageView, scoreView, buttonView)

		return m.styles.NormalBorder(m.returnButton.Focused() || m.restartButton.Focused()).
			Width(m.width).
			Height(m.height).
			Render(content)
	}
	panic("unreachable")
}
