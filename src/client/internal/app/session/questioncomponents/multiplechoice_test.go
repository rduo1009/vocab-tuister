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

type modelMC struct {
	QuestionComponent *MultipleChoiceQuestionModel
	CurrentMsg        tea.Msg
	RemovedNavigables []navigator.Navigable
}

func (m modelMC) Init() tea.Cmd {
	return m.QuestionComponent.Init()
}

func (m modelMC) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
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

func (m modelMC) View() tea.View {
	return tea.NewView(m.QuestionComponent.View())
}

func TestMultipleChoiceLatToEng(t *testing.T) {
	q := questions.MultipleChoiceLatToEngQuestion{
		Prompt:  "prompt",
		Choices: []string{"foo", "bar", "baz"},
		Answer:  "baz",
	}
	qc := NewMultipleChoiceQuestionModel(&q)

	view := qc.View()
	assert.Contains(t, view, "Translate")
	assert.Contains(t, view, "to English:")
	assert.Contains(t, view, "prompt")
	assert.Contains(t, view, "foo")
	assert.Contains(t, view, "bar")
	assert.Contains(t, view, "baz")

	golden.RequireEqual(t, []byte(view))
}

func TestMultipleChoiceEngToLat(t *testing.T) {
	q := questions.MultipleChoiceEngToLatQuestion{
		Prompt:  "prompt",
		Choices: []string{"foo", "bar", "baz"},
		Answer:  "baz",
	}
	qc := NewMultipleChoiceQuestionModel(&q)

	view := qc.View()
	assert.Contains(t, view, "Translate")
	assert.Contains(t, view, "to Latin")
	assert.Contains(t, view, "prompt")
	assert.Contains(t, view, "foo")
	assert.Contains(t, view, "bar")
	assert.Contains(t, view, "baz")

	golden.RequireEqual(t, []byte(view))
}

func TestMultipleChoiceCorrect(t *testing.T) { //nolint:dupl
	q := questions.MultipleChoiceLatToEngQuestion{
		Prompt:  "prompt",
		Choices: []string{"foo", "bar", "baz"},
		Answer:  "baz",
	}
	qc := NewMultipleChoiceQuestionModel(&q)

	m := modelMC{QuestionComponent: qc}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	// simulate selecting final option (correct)
	m.QuestionComponent.options[0].Blur()
	m.QuestionComponent.options[2].Focus()

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})
	time.Sleep(10 * time.Millisecond)
	tm.Quit()

	fm := tm.FinalModel(t)
	m, ok := fm.(modelMC)
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

func TestMultipleChoiceIncorrect(t *testing.T) { //nolint:dupl
	q := questions.MultipleChoiceLatToEngQuestion{
		Prompt:  "prompt",
		Choices: []string{"foo", "bar", "baz"},
		Answer:  "baz",
	}
	qc := NewMultipleChoiceQuestionModel(&q)

	m := modelMC{QuestionComponent: qc}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	// simulate selecting second option (incorrect)
	m.QuestionComponent.options[0].Blur()
	m.QuestionComponent.options[1].Focus()

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})
	time.Sleep(10 * time.Millisecond)
	tm.Quit()

	fm := tm.FinalModel(t)
	m, ok := fm.(modelMC)
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

	golden.RequireEqual(t, []byte(m.QuestionComponent.View()))
}

func TestMultipleChoiceNextQuestion(t *testing.T) {
	q := questions.MultipleChoiceLatToEngQuestion{
		Prompt:  "prompt",
		Choices: []string{"foo", "bar", "baz"},
		Answer:  "baz",
	}
	qc := NewMultipleChoiceQuestionModel(&q)

	m := modelMC{QuestionComponent: qc}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	// simulate selecting final option (correct)
	m.QuestionComponent.options[0].Blur()
	m.QuestionComponent.options[2].Focus()

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})
	time.Sleep(10 * time.Millisecond)

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})
	time.Sleep(10 * time.Millisecond)
	tm.Quit()

	fm := tm.FinalModel(t)
	m, ok := fm.(modelMC)
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
	assert.Len(t, m.RemovedNavigables, 3)
}
