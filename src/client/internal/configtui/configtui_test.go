package configtui_test

import (
	"flag"
	"io"
	"os"
	"path/filepath"
	"testing"
	"time"

	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/x/exp/teatest/v2"
	"github.com/stretchr/testify/assert"

	"github.com/rduo1009/vocab-tuister/src/client/internal/configtui"
)

const (
	outputConfigFile = "output-config.json"

	firstPageColumns = 20
	numberOfPages    = 9

	millisecondDelay = 50
)

func readBts(tb testing.TB, r io.Reader) []byte {
	tb.Helper()

	bts, err := io.ReadAll(r)
	if err != nil {
		tb.Fatal(err)
	}
	return bts
}

func goldenValue(t *testing.T, goldenFile string, actual []byte, update bool) []byte {
	t.Helper()

	goldenPath := filepath.Join("testdata", goldenFile+".golden")

	f, err := os.OpenFile(goldenPath, os.O_RDWR|os.O_CREATE, 0o644)
	if err != nil {
		t.Fatalf("error opening file %s: %s", goldenPath, err)
	}
	defer f.Close()

	if update {
		_, err := f.Write(actual)
		if err != nil {
			t.Fatalf("error writing to file %s: %s", goldenPath, err)
		}

		return actual
	}

	content, err := io.ReadAll(f)
	if err != nil {
		t.Fatalf("error opening file %s: %s", goldenPath, err)
	}
	return content
}

func setUpTUI(t *testing.T) (*teatest.TestModel, string) {
	t.Helper()

	outputConfigFilepath := filepath.Join(t.TempDir(), outputConfigFile)
	m := configtui.InitialModel(outputConfigFilepath)
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(300, 100))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})
	time.Sleep(time.Millisecond * millisecondDelay)

	return tm, outputConfigFilepath
}

func sendKeyWithDelay(tm *teatest.TestModel, msg rune) {
	tm.Send(tea.KeyPressMsg{Code: msg})
	time.Sleep(time.Millisecond * millisecondDelay)
}

func TestMain(m *testing.M) {
	flag.Parse()
	os.Exit(m.Run())
}

func TestFirstScreen(t *testing.T) {
	tm, _ := setUpTUI(t)

	tm.Quit()
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestAllScreens(t *testing.T) {
	tm, _ := setUpTUI(t)

	for range numberOfPages - 1 {
		sendKeyWithDelay(tm, tea.KeyRight)
	}

	tm.Quit()
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestNoMoveLeft(t *testing.T) {
	tm, _ := setUpTUI(t)

	sendKeyWithDelay(tm, tea.KeyLeft)

	tm.Quit()
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestNoMoveUp(t *testing.T) {
	tm, _ := setUpTUI(t)

	sendKeyWithDelay(tm, tea.KeyUp)

	tm.Quit()
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestNoMoveDown(t *testing.T) {
	tm, _ := setUpTUI(t)

	for range firstPageColumns {
		sendKeyWithDelay(tm, tea.KeyDown)
	}

	tm.Quit()
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestMoveRight(t *testing.T) {
	tm, _ := setUpTUI(t)

	sendKeyWithDelay(tm, tea.KeyRight)

	tm.Quit()
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestMoveLeft(t *testing.T) {
	tm, _ := setUpTUI(t)

	sendKeyWithDelay(tm, tea.KeyRight)
	sendKeyWithDelay(tm, tea.KeyRight)
	sendKeyWithDelay(tm, tea.KeyLeft)

	tm.Quit()
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestSelect(t *testing.T) {
	tm, _ := setUpTUI(t)

	sendKeyWithDelay(tm, tea.KeySpace)
	sendKeyWithDelay(tm, tea.KeyDown)
	sendKeyWithDelay(tm, tea.KeyReturn)
	sendKeyWithDelay(tm, tea.KeyDown)

	sendKeyWithDelay(tm, tea.KeyRight)
	sendKeyWithDelay(tm, tea.KeySpace)
	sendKeyWithDelay(tm, tea.KeyLeft)

	tm.Quit()
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestDeselect(t *testing.T) {
	tm, _ := setUpTUI(t)

	sendKeyWithDelay(tm, tea.KeySpace)
	sendKeyWithDelay(tm, tea.KeyDown)
	sendKeyWithDelay(tm, tea.KeyReturn)
	sendKeyWithDelay(tm, tea.KeyDown)

	sendKeyWithDelay(tm, tea.KeyRight)
	sendKeyWithDelay(tm, tea.KeyLeft)

	sendKeyWithDelay(tm, tea.KeySpace)
	sendKeyWithDelay(tm, tea.KeyDown)
	sendKeyWithDelay(tm, tea.KeyReturn)
	sendKeyWithDelay(tm, tea.KeyDown)

	tm.Quit()
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestNoNumber(t *testing.T) {
	tm, _ := setUpTUI(t)

	for range numberOfPages {
		sendKeyWithDelay(tm, tea.KeyRight)
	}

	tm.WaitFinished(t, teatest.WithFinalTimeout(time.Second*3))
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestInvalidNumber(t *testing.T) {
	tm, _ := setUpTUI(t)

	for range numberOfPages - 1 {
		sendKeyWithDelay(tm, tea.KeyRight)
	}
	tm.Type("abc")
	sendKeyWithDelay(tm, tea.KeyRight)

	tm.WaitFinished(t, teatest.WithFinalTimeout(time.Second*3))
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestComplete(t *testing.T) {
	tm, filePath := setUpTUI(t)
	update := flag.Lookup("update").Value.(flag.Getter).Get().(bool)

	// Select (or deselect) first and third options of each
	for range numberOfPages - 1 {
		sendKeyWithDelay(tm, tea.KeySpace)
		sendKeyWithDelay(tm, tea.KeyDown)
		sendKeyWithDelay(tm, tea.KeyDown)
		sendKeyWithDelay(tm, tea.KeyReturn)

		sendKeyWithDelay(tm, tea.KeyRight)
	}

	// Type number of questions for multiple-choice questions
	tm.Type("3")
	sendKeyWithDelay(tm, tea.KeyRight)

	// Test program output
	tm.WaitFinished(t, teatest.WithFinalTimeout(time.Second*3))
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)

	// Test JSON output
	got, err := os.ReadFile(filePath)
	if err != nil {
		t.Fatalf("error opening file %s: %s", filePath, err)
	}
	want := goldenValue(t, "TestCompleteJson", got, update)
	assert.Equal(t, got, want)
}
