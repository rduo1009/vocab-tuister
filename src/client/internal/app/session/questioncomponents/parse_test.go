package questioncomponents

import (
	"testing"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/exp/golden"
	"github.com/charmbracelet/x/exp/teatest/v2"
	"github.com/stretchr/testify/assert"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions/endingcomponents"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/dropdown"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
)

type modelPS struct {
	QuestionComponent *ParseQuestionModel
	CurrentMsg        tea.Msg
	RemovedNavigables []navigator.Navigable
}

func (m modelPS) Init() tea.Cmd {
	return m.QuestionComponent.Init()
}

func (m modelPS) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
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

func (m modelPS) View() tea.View {
	return tea.NewView(m.QuestionComponent.View())
}

func TestParse(t *testing.T) {
	q := questions.ParseWordLatToCompQuestion{
		Prompt:          "prompt",
		DictionaryEntry: "dictionary entry",
		MainAnswer: endingcomponents.EndingComponents{
			Case:   endingcomponents.Genitive,
			Number: endingcomponents.Plural,
			Gender: endingcomponents.Neuter,
		},
		Answers: []endingcomponents.EndingComponents{{
			Case:   endingcomponents.Genitive,
			Number: endingcomponents.Plural,
			Gender: endingcomponents.Neuter,
		}},
	}
	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	qc := NewParseQuestionModel(&q, &s)

	view := qc.View()
	assert.Contains(t, view, "Parse")
	assert.Contains(t, view, "this Latin word:")
	assert.Contains(t, view, "prompt")
	assert.Contains(t, view, "nominative")
	assert.Contains(t, view, "singular")
	assert.Contains(t, view, "masculine")

	golden.RequireEqual(t, []byte(view))
}

// NOTE: Wrangling the dropdowns themselves is too tricky and will be left to e2e testing.
// So manually changing `LastSelected` in each dropdown (as the dropdowns themselves would normally do) so that the
// view is still correct

func TestParseCorrect(t *testing.T) {
	tests := []struct {
		name      string
		selection endingcomponents.EndingComponents
		expect    []string
	}{
		{
			name: "TestParseCorrectMain",
			selection: endingcomponents.EndingComponents{
				Case:   endingcomponents.Genitive,
				Number: endingcomponents.Plural,
				Gender: endingcomponents.Neuter,
			},
			expect: []string{"genitive", "plural", "neuter"},
		},
		{
			name: "TestParseCorrectAlt",
			selection: endingcomponents.EndingComponents{
				Case:   endingcomponents.Genitive,
				Number: endingcomponents.Plural,
				Gender: endingcomponents.Feminine,
			},
			expect: []string{"genitive", "plural", "feminine"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			q := questions.ParseWordLatToCompQuestion{
				Prompt: "prompt",
				MainAnswer: endingcomponents.EndingComponents{
					Case:   endingcomponents.Genitive,
					Number: endingcomponents.Plural,
					Gender: endingcomponents.Neuter,
				},
				Answers: []endingcomponents.EndingComponents{{
					Case:   endingcomponents.Genitive,
					Number: endingcomponents.Plural,
					Gender: endingcomponents.Neuter,
				}, {
					Case:   endingcomponents.Genitive,
					Number: endingcomponents.Plural,
					Gender: endingcomponents.Feminine,
				}},
			}
			s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
			qc := NewParseQuestionModel(&q, &s)

			m := modelPS{QuestionComponent: qc}
			tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
			t.Cleanup(func() {
				if err := tm.Quit(); err != nil {
					t.Fatal(err)
				}
			})

			// simulate dropdown selections
			tm.Send(dropdown.PickedMsg{ID: "parsequestionDropdown0", ChosenItem: tt.selection.Case})
			m.QuestionComponent.Dropdowns[0].LastSelected = tt.selection.Case

			tm.Send(dropdown.PickedMsg{ID: "parsequestionDropdown1", ChosenItem: tt.selection.Number})
			m.QuestionComponent.Dropdowns[1].LastSelected = tt.selection.Number

			tm.Send(dropdown.PickedMsg{ID: "parsequestionDropdown2", ChosenItem: tt.selection.Gender})
			m.QuestionComponent.Dropdowns[2].LastSelected = tt.selection.Gender

			tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter, Mod: tea.ModCtrl})
			time.Sleep(10 * time.Millisecond)
			tm.Quit()

			fm := tm.FinalModel(t)
			m, ok := fm.(modelPS)
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

			view := m.QuestionComponent.View()
			for _, s := range tt.expect {
				assert.Contains(t, view, s)
			}

			golden.RequireEqual(t, []byte(view))
		})
	}
}

func TestParseIncorrect(t *testing.T) {
	q := questions.ParseWordLatToCompQuestion{
		Prompt: "prompt",
		MainAnswer: endingcomponents.EndingComponents{
			Case:   endingcomponents.Genitive,
			Number: endingcomponents.Plural,
			Gender: endingcomponents.Neuter,
		},
		Answers: []endingcomponents.EndingComponents{{
			Case:   endingcomponents.Genitive,
			Number: endingcomponents.Plural,
			Gender: endingcomponents.Neuter,
		}, {
			Case:   endingcomponents.Genitive,
			Number: endingcomponents.Plural,
			Gender: endingcomponents.Feminine,
		}},
	}
	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	qc := NewParseQuestionModel(&q, &s)

	m := modelPS{QuestionComponent: qc}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	// incorrect
	tm.Send(dropdown.PickedMsg{ID: "parsequestionDropdown0", ChosenItem: endingcomponents.Genitive})
	m.QuestionComponent.Dropdowns[0].LastSelected = endingcomponents.Genitive
	tm.Send(dropdown.PickedMsg{ID: "parsequestionDropdown1", ChosenItem: endingcomponents.Plural})
	m.QuestionComponent.Dropdowns[1].LastSelected = endingcomponents.Plural
	tm.Send(dropdown.PickedMsg{ID: "parsequestionDropdown2", ChosenItem: endingcomponents.Masculine})
	m.QuestionComponent.Dropdowns[2].LastSelected = endingcomponents.Masculine

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter, Mod: tea.ModCtrl})
	time.Sleep(10 * time.Millisecond)
	tm.Quit()

	fm := tm.FinalModel(t)
	m, ok := fm.(modelPS)
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

	view := m.QuestionComponent.View()
	assert.Contains(t, view, "genitive")
	assert.Contains(t, view, "plural")
	assert.Contains(t, view, "masculine")
	assert.Contains(t, view, "genitive plural neuter")
	assert.NotContains(t, view, "feminine")

	golden.RequireEqual(t, []byte(view))
}

func TestParseNextQuestion(t *testing.T) {
	q := questions.ParseWordLatToCompQuestion{
		Prompt: "prompt",
		MainAnswer: endingcomponents.EndingComponents{
			Case:   endingcomponents.Genitive,
			Number: endingcomponents.Plural,
			Gender: endingcomponents.Neuter,
		},
		Answers: []endingcomponents.EndingComponents{{
			Case:   endingcomponents.Genitive,
			Number: endingcomponents.Plural,
			Gender: endingcomponents.Neuter,
		}},
	}
	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	qc := NewParseQuestionModel(&q, &s)

	m := modelPS{QuestionComponent: qc}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	// correct
	tm.Send(dropdown.PickedMsg{ID: "parsequestionDropdown0", ChosenItem: endingcomponents.Genitive})
	tm.Send(dropdown.PickedMsg{ID: "parsequestionDropdown1", ChosenItem: endingcomponents.Plural})
	tm.Send(dropdown.PickedMsg{ID: "parsequestionDropdown2", ChosenItem: endingcomponents.Neuter})

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter, Mod: tea.ModCtrl})
	time.Sleep(10 * time.Millisecond)

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})
	time.Sleep(10 * time.Millisecond)
	tm.Quit()

	fm := tm.FinalModel(t)
	m, ok := fm.(modelPS)
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
