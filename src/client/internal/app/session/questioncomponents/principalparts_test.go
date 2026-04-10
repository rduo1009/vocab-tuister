package questioncomponents

import (
	"testing"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/exp/golden"
	"github.com/charmbracelet/x/exp/teatest/v2"
	"github.com/stretchr/testify/assert"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
)

type modelPP struct {
	QuestionComponent *PrincipalPartsQuestionModel
	CurrentMsg        tea.Msg
	RemovedNavigables []navigator.Navigable
}

func (m modelPP) Init() tea.Cmd {
	return m.QuestionComponent.Init()
}

func (m modelPP) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case QuestionAnsweredMsg:
		m.CurrentMsg = msg
	case NextQuestionMsg:
		m.CurrentMsg = msg
	case navigator.RemoveNavigableMsg:
		m.RemovedNavigables = msg.Components
	}

	var cmd tea.Cmd
	_, cmd = m.QuestionComponent.Update(msg)

	return m, cmd
}

func (m modelPP) View() tea.View {
	return tea.NewView(m.QuestionComponent.View())
}

func TestPrincipalParts(t *testing.T) {
	q := questions.PrincipalPartsQuestion{
		Prompt:         "prompt",
		PrincipalParts: []string{"foo", "bar", "baz", "qux"},
	}
	qc := NewPrincipalPartsQuestionModel(&q)

	view := qc.View()
	assert.Contains(t, view, "Principal parts")
	assert.Contains(t, view, "of")
	assert.Contains(t, view, "prompt")

	golden.RequireEqual(t, []byte(view))
}

func TestPrincipalPartsCorrect(t *testing.T) {
	q := questions.PrincipalPartsQuestion{
		Prompt:         "prompt",
		PrincipalParts: []string{"foo", "bar", "baz", "qux"},
	}
	qc := NewPrincipalPartsQuestionModel(&q)

	m := modelPP{QuestionComponent: qc}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	// all correct
	m.QuestionComponent.textinputs[0].Focus()
	tm.Type("foo")
	time.Sleep(10 * time.Millisecond)
	m.QuestionComponent.textinputs[0].Blur()
	m.QuestionComponent.textinputs[1].Focus()
	tm.Type("bar")
	time.Sleep(10 * time.Millisecond)
	m.QuestionComponent.textinputs[1].Blur()
	m.QuestionComponent.textinputs[2].Focus()
	tm.Type("baz")
	time.Sleep(10 * time.Millisecond)
	m.QuestionComponent.textinputs[2].Blur()
	m.QuestionComponent.textinputs[3].Focus()
	tm.Type("qux")
	time.Sleep(10 * time.Millisecond)

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})
	time.Sleep(10 * time.Millisecond)
	tm.Quit()

	fm := tm.FinalModel(t)
	m, ok := fm.(modelPP)
	if !ok {
		t.Fatalf("final model have the wrong type: %T", fm)
	}

	assert.IsTypef(
		t,
		QuestionAnsweredMsg{},
		m.CurrentMsg,
		"expected type QuestionAnsweredMsg, got type %T",
		m.CurrentMsg,
	)
	assert.Equalf(
		t,
		Correct,
		m.QuestionComponent.QuestionStatus(),
		"expected Correct, got %s",
		m.QuestionComponent.QuestionStatus(),
	)

	golden.RequireEqual(t, []byte(m.QuestionComponent.View()))
}

func TestPrincipalPartsIncorrect(t *testing.T) {
	q := questions.PrincipalPartsQuestion{
		Prompt:         "prompt",
		PrincipalParts: []string{"foo", "bar", "baz", "qux"},
	}
	qc := NewPrincipalPartsQuestionModel(&q)

	m := modelPP{QuestionComponent: qc}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	// two correct, two incorrect
	m.QuestionComponent.textinputs[0].Focus()
	tm.Type("foo")
	time.Sleep(10 * time.Millisecond)
	m.QuestionComponent.textinputs[0].Blur()
	m.QuestionComponent.textinputs[1].Focus()
	tm.Type("wrong")
	time.Sleep(10 * time.Millisecond)
	m.QuestionComponent.textinputs[1].Blur()
	m.QuestionComponent.textinputs[2].Focus()
	tm.Type("baz")
	time.Sleep(10 * time.Millisecond)
	m.QuestionComponent.textinputs[2].Blur()
	m.QuestionComponent.textinputs[3].Focus()
	tm.Type("wrong")
	time.Sleep(10 * time.Millisecond)

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})
	time.Sleep(10 * time.Millisecond)
	tm.Quit()

	fm := tm.FinalModel(t)
	m, ok := fm.(modelPP)
	if !ok {
		t.Fatalf("final model have the wrong type: %T", fm)
	}

	assert.IsTypef(
		t,
		QuestionAnsweredMsg{},
		m.CurrentMsg,
		"expected type QuestionAnsweredMsg, got type %T",
		m.CurrentMsg,
	)
	assert.Equalf(
		t,
		Incorrect,
		m.QuestionComponent.QuestionStatus(),
		"expected Incorrect, got %s",
		m.QuestionComponent.QuestionStatus(),
	)
	assert.Contains(t, m.QuestionComponent.View(), "wrong")
	assert.Contains(t, m.QuestionComponent.View(), "bar")
	assert.Contains(t, m.QuestionComponent.View(), "qux")

	golden.RequireEqual(t, []byte(m.QuestionComponent.View()))
}

func TestPrincipalPartsNextQuestion(t *testing.T) {
	q := questions.PrincipalPartsQuestion{
		Prompt:         "prompt",
		PrincipalParts: []string{"foo", "bar", "baz", "qux"},
	}
	qc := NewPrincipalPartsQuestionModel(&q)

	m := modelPP{QuestionComponent: qc}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	// all correct
	m.QuestionComponent.textinputs[0].Focus()
	tm.Type("foo")
	time.Sleep(10 * time.Millisecond)
	m.QuestionComponent.textinputs[0].Blur()
	m.QuestionComponent.textinputs[1].Focus()
	tm.Type("bar")
	time.Sleep(10 * time.Millisecond)
	m.QuestionComponent.textinputs[1].Blur()
	m.QuestionComponent.textinputs[2].Focus()
	tm.Type("baz")
	time.Sleep(10 * time.Millisecond)
	m.QuestionComponent.textinputs[2].Blur()
	m.QuestionComponent.textinputs[3].Focus()
	tm.Type("qux")
	time.Sleep(10 * time.Millisecond)

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})
	time.Sleep(10 * time.Millisecond)

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})
	time.Sleep(10 * time.Millisecond)
	tm.Quit()

	fm := tm.FinalModel(t)
	m, ok := fm.(modelPP)
	if !ok {
		t.Fatalf("final model have the wrong type: %T", fm)
	}

	assert.IsTypef(
		t,
		NextQuestionMsg{},
		m.CurrentMsg,
		"expected type QuestionAnsweredMsg, got type %T",
		m.CurrentMsg,
	)
	assert.Len(t, m.RemovedNavigables, 4)
}
