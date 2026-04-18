package saveas_test

import (
	"bytes"
	"os"
	"path/filepath"
	"testing"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/exp/golden"
	"github.com/charmbracelet/x/exp/teatest/v2"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/saveas"
	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
)

const id = "testingSaveAs"

// model wraps saveas.Model so it satisfies tea.Model for teatest.
// It captures the most recent SelectedMsg or ExitMsg for later assertions.
type model struct {
	SaveAs     *saveas.Model
	CurrentMsg tea.Msg
}

func (m model) Init() tea.Cmd {
	return m.SaveAs.Init()
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg.(type) {
	case saveas.SelectedMsg, saveas.ExitMsg:
		m.CurrentMsg = msg
		return m, tea.Quit
	}

	var cmd tea.Cmd
	_, cmd = m.SaveAs.Update(msg)

	return m, cmd
}

// View passes fixed screen dimensions so the test model satisfies tea.Model.
func (m model) View() tea.View {
	view, _, _ := m.SaveAs.View(100, 30)
	return tea.NewView(view)
}

// makeTempDir creates a temporary directory containing a few files and
// sub-directories suitable for saveas tests.
func makeTempDir(tb testing.TB) string {
	tb.Helper()

	dir := tb.TempDir()

	// Create a couple of plain text files at the top level.
	require.NoError(tb, os.WriteFile(filepath.Join(dir, "alpha.txt"), []byte("alpha"), 0o644))
	require.NoError(tb, os.WriteFile(filepath.Join(dir, "beta.txt"), []byte("beta"), 0o644))

	// Create a sub-directory with its own file.
	subDir := filepath.Join(dir, "subdir")
	require.NoError(tb, os.Mkdir(subDir, 0o755))
	require.NoError(tb, os.WriteFile(filepath.Join(subDir, "gamma.txt"), []byte("gamma"), 0o644))

	return dir
}

// TestSaveAs checks the initial rendered output of the saveas component.
// Run with -update to regenerate the golden file.
func TestSaveAs(t *testing.T) {
	if os.Getenv("CI") != "" {
		t.Skip("Skipping test in CI environment")
	}

	dir := makeTempDir(t)

	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	sa := saveas.New(id, dir, &s)
	sa.SetWidth(160)
	sa.SetHeight(15)

	m := model{SaveAs: sa}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	teatest.WaitFor(t, tm.Output(), func(bts []byte) bool {
		return bytes.Contains(bts, []byte("alpha.txt"))
	}, teatest.WithCheckInterval(time.Millisecond*50), teatest.WithDuration(time.Second*3))

	if err := tm.Quit(); err != nil {
		t.Fatal(err)
	}

	finalModel := tm.FinalModel(t).(model)
	// Update path to common string for consistent golden file
	finalModel.SaveAs.Update(saveas.SetPathMsg{ID: id, Path: "/foo/bar"})
	finalView, _, _ := finalModel.SaveAs.View(70, 30)
	golden.RequireEqual(t, []byte(finalView))
}

func TestSaveAsExit(t *testing.T) {
	dir := makeTempDir(t)

	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	sa := saveas.New(id, dir, &s)
	m := model{SaveAs: sa}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	tm.Send(tea.KeyPressMsg{Code: tea.KeyEsc})
	tm.WaitFinished(t)

	assert.Equal(t, saveas.ExitMsg{ID: id}, tm.FinalModel(t).(model).CurrentMsg)
}

func TestSaveAsSubmitEmptyFilename(t *testing.T) {
	dir := makeTempDir(t)

	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	sa := saveas.New(id, dir, &s)
	sa.SetWidth(160)
	sa.SetHeight(10)

	m := model{SaveAs: sa}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	tm.Send(tea.KeyPressMsg{Code: tea.KeyTab})   // Focus input
	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter}) // Attempt to submit empty

	if err := tm.Quit(); err != nil {
		t.Fatal(err)
	}

	finalModel := tm.FinalModel(t).(model)
	assert.Nil(t, finalModel.CurrentMsg)

	view, _, _ := finalModel.SaveAs.View(70, 30)
	assert.Contains(t, view, "filename cannot be empty")
}

func TestSaveAsSubmitInvalidAllowedTypes(t *testing.T) {
	dir := makeTempDir(t)

	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	sa := saveas.New(id, dir, &s, ".csv") // Only allow .csv
	sa.SetWidth(160)
	sa.SetHeight(10)

	m := model{SaveAs: sa}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	tm.Send(tea.KeyPressMsg{Code: tea.KeyTab}) // Focus
	for _, c := range "file.txt" {
		tm.Send(tea.KeyPressMsg{Code: rune(c), Text: string(c)})
	}
	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})

	if err := tm.Quit(); err != nil {
		t.Fatal(err)
	}

	finalModel := tm.FinalModel(t).(model)
	assert.Nil(t, finalModel.CurrentMsg)

	view, _, _ := finalModel.SaveAs.View(70, 30)
	assert.Contains(t, view, "invalid file type")
}

func TestSaveAsSubmitWithNewFile(t *testing.T) {
	dir := makeTempDir(t)

	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	sa := saveas.New(id, dir, &s)

	m := model{SaveAs: sa}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	tm.Send(tea.KeyPressMsg{Code: tea.KeyTab}) // Focus
	for _, c := range "newfile.txt" {
		tm.Send(tea.KeyPressMsg{Code: rune(c), Text: string(c)})
	}
	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter})

	tm.WaitFinished(t)

	expectedMsg := saveas.SelectedMsg{
		ID:        id,
		Path:      filepath.Join(dir, "newfile.txt"),
		Overwrite: false,
	}

	assert.Equal(t, expectedMsg, tm.FinalModel(t).(model).CurrentMsg)
}

func TestSaveAsSubmitWithExistingFileAndConfirm(t *testing.T) {
	dir := makeTempDir(t)

	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	sa := saveas.New(id, dir, &s)
	sa.SetWidth(160)
	sa.SetHeight(15)

	m := model{SaveAs: sa}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(100, 40))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	tm.Send(tea.KeyPressMsg{Code: tea.KeyTab}) // Focus
	for _, c := range "alpha.txt" {
		tm.Send(tea.KeyPressMsg{Code: rune(c), Text: string(c)})
	}
	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter}) // Submit "alpha.txt"

	teatest.WaitFor(t, tm.Output(), func(bts []byte) bool {
		return bytes.Contains(bts, []byte("Overwrite?"))
	}, teatest.WithCheckInterval(time.Millisecond*50), teatest.WithDuration(time.Second*3))

	// Now press 'y' to confirm overwrite
	tm.Send(tea.KeyPressMsg{Code: 'y', Text: "y"})

	tm.WaitFinished(t)

	expectedMsg := saveas.SelectedMsg{
		ID:        id,
		Path:      filepath.Join(dir, "alpha.txt"),
		Overwrite: true,
	}

	assert.Equal(t, expectedMsg, tm.FinalModel(t).(model).CurrentMsg)
}

func TestSaveAsSubmitWithExistingFileAndDeny(t *testing.T) {
	dir := makeTempDir(t)

	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	sa := saveas.New(id, dir, &s)
	sa.SetWidth(160)
	sa.SetHeight(15)

	m := model{SaveAs: sa}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(100, 40))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	tm.Send(tea.KeyPressMsg{Code: tea.KeyTab}) // Focus
	for _, c := range "alpha.txt" {
		tm.Send(tea.KeyPressMsg{Code: rune(c), Text: string(c)})
	}
	tm.Send(tea.KeyPressMsg{Code: tea.KeyEnter}) // Submit "alpha.txt"

	teatest.WaitFor(t, tm.Output(), func(bts []byte) bool {
		return bytes.Contains(bts, []byte("Overwrite?"))
	}, teatest.WithCheckInterval(time.Millisecond*50), teatest.WithDuration(time.Second*3))

	// Deny with 'n'
	tm.Send(tea.KeyPressMsg{Code: 'n', Text: "n"})

	// Give a bit of time to make sure it processes before we quit
	time.Sleep(100 * time.Millisecond)

	if err := tm.Quit(); err != nil {
		t.Fatal(err)
	}

	finalModel := tm.FinalModel(t).(model)

	// Ensure we did NOT exit or emit a selected message
	assert.Nil(t, finalModel.CurrentMsg)

	// Confirm we are no longer in overwrite confirmation mode
	view, _, _ := finalModel.SaveAs.View(70, 30)
	assert.NotContains(t, view, "Overwrite?")
}

func TestSaveAsSetPath(t *testing.T) {
	dir := makeTempDir(t)

	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	sa := saveas.New(id, dir, &s)
	sa.SetWidth(160)
	sa.SetHeight(10)

	m := model{SaveAs: sa}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	newDir := t.TempDir()
	tm.Send(saveas.SetPathMsg{ID: id, Path: newDir})

	if err := tm.Quit(); err != nil {
		t.Fatal(err)
	}

	finalModel := tm.FinalModel(t).(model)

	view, _, _ := finalModel.SaveAs.View(70, 30)
	assert.Contains(t, view, newDir)
}

func TestSaveAsSetPathWrongID(t *testing.T) {
	dir := makeTempDir(t)

	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	sa := saveas.New(id, dir, &s)
	sa.SetWidth(160)
	sa.SetHeight(10)

	m := model{SaveAs: sa}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	wrongDir := t.TempDir()
	// Send a SetPathMsg with a different ID
	tm.Send(saveas.SetPathMsg{ID: "differentID", Path: wrongDir})

	if err := tm.Quit(); err != nil {
		t.Fatal(err)
	}

	finalModel := tm.FinalModel(t).(model)

	view, _, _ := finalModel.SaveAs.View(70, 30)
	assert.Contains(t, view, dir)
	assert.NotContains(t, view, wrongDir)
}

func TestSaveAsKeyMap(t *testing.T) {
	dir := makeTempDir(t)
	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	sa := saveas.New(id, dir, &s)

	km := sa.KeyMap()
	assert.NotNil(t, km)
	assert.NotEmpty(t, km.ShortHelp())
	assert.NotEmpty(t, km.FullHelp())
}

func TestSaveAsViewCentred(t *testing.T) {
	dir := makeTempDir(t)

	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	sa := saveas.New(id, dir, &s)
	sa.SetWidth(40)
	sa.SetHeight(10)

	const screenW, screenH = 120, 40

	view, x, y := sa.View(screenW, screenH)

	assert.NotEmpty(t, view)
	assert.GreaterOrEqual(t, x, 0)
	assert.GreaterOrEqual(t, y, 0)
}
