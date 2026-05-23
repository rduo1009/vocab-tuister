package questioncomponents

import (
	"testing"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/exp/teatest/v2"
	"github.com/stretchr/testify/assert"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions/endingcomponents"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/dropdown"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"
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
	q := questions.ParseWordLatToCompQuestion{ParseWordLatToCompQuestion: &pb.ParseWordLatToCompQuestion{
		Prompt:          "prompt",
		DictionaryEntry: "dictionary entry",
		MainAnswer: &pb.EndingComponents{
			Case:   pb.Case_CASE_GENITIVE,
			Number: pb.Number_NUMBER_PLURAL,
			Gender: pb.Gender_GENDER_NEUTER,
		},
		Answers: []*pb.EndingComponents{{
			Case:   pb.Case_CASE_GENITIVE,
			Number: pb.Number_NUMBER_PLURAL,
			Gender: pb.Gender_GENDER_NEUTER,
		}},
	}}
	qc := NewParseQuestionModel(&q, newStyles())

	view := qc.View()
	assert.Contains(t, view, "Parse")
	assert.Contains(t, view, "this Latin word:")
	assert.Contains(t, view, "prompt")
	assert.Contains(t, view, "nominative")
	assert.Contains(t, view, "singular")
	assert.Contains(t, view, "masculine")

	requireGoldenWithSuffix(t, []byte(view))
}

// NOTE: Wrangling the dropdowns themselves is too tricky and will be left to e2e testing.
// So manually changing `LastSelected` in each dropdown (as the dropdowns themselves would normally do) so that the
// view is still correct

func TestParseCorrect(t *testing.T) {
	tests := []struct {
		name      string
		selection *pb.EndingComponents
		expect    []string
	}{
		{
			name: "TestParseCorrectMain",
			selection: &pb.EndingComponents{
				Case:          pb.Case_CASE_GENITIVE,
				Number:        pb.Number_NUMBER_PLURAL,
				Gender:        pb.Gender_GENDER_NEUTER,
				DisplayString: "genitive plural neuter",
			},
			expect: []string{"genitive", "plural", "neuter"},
		},
		{
			name: "TestParseCorrectAlt",
			selection: &pb.EndingComponents{
				Case:          pb.Case_CASE_GENITIVE,
				Number:        pb.Number_NUMBER_PLURAL,
				Gender:        pb.Gender_GENDER_FEMININE,
				DisplayString: "genitive plural feminine",
			},
			expect: []string{"genitive", "plural", "feminine"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			q := questions.ParseWordLatToCompQuestion{
				ParseWordLatToCompQuestion: &pb.ParseWordLatToCompQuestion{
					Prompt: "prompt",
					MainAnswer: &pb.EndingComponents{
						Case:          pb.Case_CASE_GENITIVE,
						Number:        pb.Number_NUMBER_PLURAL,
						Gender:        pb.Gender_GENDER_NEUTER,
						DisplayString: "genitive plural neuter",
					},
					Answers: []*pb.EndingComponents{{
						Case:          pb.Case_CASE_GENITIVE,
						Number:        pb.Number_NUMBER_PLURAL,
						Gender:        pb.Gender_GENDER_NEUTER,
						DisplayString: "genitive plural neuter",
					}, {
						Case:          pb.Case_CASE_GENITIVE,
						Number:        pb.Number_NUMBER_PLURAL,
						Gender:        pb.Gender_GENDER_FEMININE,
						DisplayString: "genitive plural feminine",
					}},
				},
			}
			qc := NewParseQuestionModel(&q, newStyles())

			m := modelPS{QuestionComponent: qc}
			tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
			t.Cleanup(func() {
				if err := tm.Quit(); err != nil {
					t.Fatal(err)
				}
			})

			tm.Send(
				dropdown.PickedMsg{
					ID:         "parsequestionDropdown0",
					ChosenItem: endingcomponents.Case(tt.selection.Case),
				},
			)
			m.QuestionComponent.Dropdowns[0].LastSelected = endingcomponents.Case(tt.selection.Case)

			tm.Send(
				dropdown.PickedMsg{
					ID:         "parsequestionDropdown1",
					ChosenItem: endingcomponents.Number(tt.selection.Number),
				},
			)
			m.QuestionComponent.Dropdowns[1].LastSelected = endingcomponents.Number(tt.selection.Number)

			tm.Send(
				dropdown.PickedMsg{
					ID:         "parsequestionDropdown2",
					ChosenItem: endingcomponents.Gender(tt.selection.Gender),
				},
			)
			m.QuestionComponent.Dropdowns[2].LastSelected = endingcomponents.Gender(tt.selection.Gender)

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

			requireGoldenWithSuffix(t, []byte(view))
		})
	}
}

func TestParseIncorrect(t *testing.T) {
	q := questions.ParseWordLatToCompQuestion{ParseWordLatToCompQuestion: &pb.ParseWordLatToCompQuestion{
		Prompt: "prompt",
		MainAnswer: &pb.EndingComponents{
			Case:          pb.Case_CASE_GENITIVE,
			Number:        pb.Number_NUMBER_PLURAL,
			Gender:        pb.Gender_GENDER_NEUTER,
			DisplayString: "genitive plural neuter",
		},
		Answers: []*pb.EndingComponents{{
			Case:          pb.Case_CASE_GENITIVE,
			Number:        pb.Number_NUMBER_PLURAL,
			Gender:        pb.Gender_GENDER_NEUTER,
			DisplayString: "genitive plural neuter",
		}, {
			Case:          pb.Case_CASE_GENITIVE,
			Number:        pb.Number_NUMBER_PLURAL,
			Gender:        pb.Gender_GENDER_FEMININE,
			DisplayString: "genitive plural feminine",
		}},
	}}
	qc := NewParseQuestionModel(&q, newStyles())

	m := modelPS{QuestionComponent: qc}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	tm.Send(
		dropdown.PickedMsg{
			ID:         "parsequestionDropdown0",
			ChosenItem: endingcomponents.Case(pb.Case_CASE_GENITIVE),
		},
	)
	m.QuestionComponent.Dropdowns[0].LastSelected = endingcomponents.Case(pb.Case_CASE_GENITIVE)

	tm.Send(
		dropdown.PickedMsg{
			ID:         "parsequestionDropdown1",
			ChosenItem: endingcomponents.Number(pb.Number_NUMBER_PLURAL),
		},
	)
	m.QuestionComponent.Dropdowns[1].LastSelected = endingcomponents.Number(pb.Number_NUMBER_PLURAL)

	tm.Send(
		dropdown.PickedMsg{
			ID:         "parsequestionDropdown2",
			ChosenItem: endingcomponents.Gender(pb.Gender_GENDER_MASCULINE),
		},
	)
	m.QuestionComponent.Dropdowns[2].LastSelected = endingcomponents.Gender(pb.Gender_GENDER_MASCULINE)

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

	requireGoldenWithSuffix(t, []byte(view))
}

func TestParseNextQuestion(t *testing.T) {
	q := questions.ParseWordLatToCompQuestion{ParseWordLatToCompQuestion: &pb.ParseWordLatToCompQuestion{
		Prompt: "prompt",
		MainAnswer: &pb.EndingComponents{
			Case:          pb.Case_CASE_GENITIVE,
			Number:        pb.Number_NUMBER_PLURAL,
			Gender:        pb.Gender_GENDER_NEUTER,
			DisplayString: "genitive plural neuter",
		},
		Answers: []*pb.EndingComponents{{
			Case:          pb.Case_CASE_GENITIVE,
			Number:        pb.Number_NUMBER_PLURAL,
			Gender:        pb.Gender_GENDER_NEUTER,
			DisplayString: "genitive plural neuter",
		}},
	}}
	qc := NewParseQuestionModel(&q, newStyles())

	m := modelPS{QuestionComponent: qc}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	tm.Send(
		dropdown.PickedMsg{
			ID:         "parsequestionDropdown0",
			ChosenItem: endingcomponents.Case(pb.Case_CASE_GENITIVE),
		},
	)
	tm.Send(
		dropdown.PickedMsg{
			ID:         "parsequestionDropdown1",
			ChosenItem: endingcomponents.Number(pb.Number_NUMBER_PLURAL),
		},
	)
	tm.Send(
		dropdown.PickedMsg{
			ID:         "parsequestionDropdown2",
			ChosenItem: endingcomponents.Gender(pb.Gender_GENDER_NEUTER),
		},
	)

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
