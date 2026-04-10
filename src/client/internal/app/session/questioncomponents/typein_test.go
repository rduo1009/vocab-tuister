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

type modelTI struct {
	QuestionComponent *TypeInQuestionModel
	CurrentMsg        tea.Msg
	RemovedNavigables []navigator.Navigable
}

func (m modelTI) Init() tea.Cmd {
	return m.QuestionComponent.Init()
}

func (m modelTI) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
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

func (m modelTI) View() tea.View {
	return tea.NewView(m.QuestionComponent.View())
}

func TestTypeInLatToEng(t *testing.T) {
	q := questions.TypeInLatToEngQuestion{
		Prompt:     "prompt",
		MainAnswer: "foo",
		Answers:    []string{"foo", "bar", "baz"},
	}
	qc := NewTypeInQuestionModel(&q)

	view := qc.View()
	assert.Contains(t, view, "Translate")
	assert.Contains(t, view, "to English:")
	assert.Contains(t, view, "prompt")

	golden.RequireEqual(t, []byte(view))
}

func TestTypeInEngToLat(t *testing.T) {
	q := questions.TypeInEngToLatQuestion{
		Prompt:     "prompt",
		MainAnswer: "foo",
		Answers:    []string{"foo", "bar", "baz"},
	}
	qc := NewTypeInQuestionModel(&q)

	view := qc.View()
	assert.Contains(t, view, "Translate")
	assert.Contains(t, view, "to Latin")
	assert.Contains(t, view, "prompt")

	golden.RequireEqual(t, []byte(view))
}

func TestTypeInCorrect(t *testing.T) {
	tests := []struct {
		name  string
		input string
	}{
		{name: "TestTypeInCorrectMain", input: "foo"},
		{name: "TestTypeInCorrectAlt", input: "bar"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			q := questions.TypeInLatToEngQuestion{
				Prompt:     "prompt",
				MainAnswer: "foo",
				Answers:    []string{"foo", "bar", "baz"},
			}
			qc := NewTypeInQuestionModel(&q)

			m := modelTI{QuestionComponent: qc}
			tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
			t.Cleanup(func() {
				if err := tm.Quit(); err != nil {
					t.Fatal(err)
				}
			})

			// simulate typing
			m.QuestionComponent.textinput.Focus()
			tm.Type(tt.input)

			tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})
			time.Sleep(10 * time.Millisecond)
			tm.Quit()

			fm := tm.FinalModel(t)
			m, ok := fm.(modelTI)
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
		})
	}
}

func TestTypeInIncorrect(t *testing.T) {
	q := questions.TypeInLatToEngQuestion{
		Prompt:     "prompt",
		MainAnswer: "foo",
		Answers:    []string{"foo", "bar", "baz"},
	}
	qc := NewTypeInQuestionModel(&q)

	m := modelTI{QuestionComponent: qc}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	// simulate typing in "qux" (incorrect)
	m.QuestionComponent.textinput.Focus()
	tm.Type("qux")

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})
	time.Sleep(10 * time.Millisecond)
	tm.Quit()

	fm := tm.FinalModel(t)
	m, ok := fm.(modelTI)
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
	assert.Contains(t, m.QuestionComponent.View(), "foo")
	assert.Contains(t, m.QuestionComponent.View(), "qux")

	golden.RequireEqual(t, []byte(m.QuestionComponent.View()))
}

func TestTypeInNextQuestion(t *testing.T) {
	q := questions.TypeInLatToEngQuestion{
		Prompt:     "prompt",
		MainAnswer: "foo",
		Answers:    []string{"foo", "bar", "baz"},
	}
	qc := NewTypeInQuestionModel(&q)

	m := modelTI{QuestionComponent: qc}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	// simulate typing in "foo" (correct)
	m.QuestionComponent.textinput.Focus()
	tm.Type("foo")

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})
	time.Sleep(10 * time.Millisecond)

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})
	time.Sleep(10 * time.Millisecond)
	tm.Quit()

	fm := tm.FinalModel(t)
	m, ok := fm.(modelTI)
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
	assert.Len(t, m.RemovedNavigables, 1)
}
