package listtui_test

import (
	"flag"
	"io"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/x/exp/teatest/v2"
	"github.com/stretchr/testify/assert"

	"github.com/rduo1009/vocab-tuister/src/client/internal/listtui"
)

const (
	outputListFile = "output-list.txt"

	millisecondDelay = 100
)

func readBts(tb testing.TB, r io.Reader) []byte {
	tb.Helper()

	bts, err := io.ReadAll(r)
	if err != nil {
		tb.Fatal(err)
	}
	return bts
}

func setUpTUI(t *testing.T) (*teatest.TestModel, string) {
	t.Helper()

	outputListFilepath := filepath.Join(t.TempDir(), outputListFile)
	m := listtui.InitialModel(outputListFilepath)
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(300, 100))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})
	time.Sleep(time.Millisecond * millisecondDelay)

	return tm, outputListFilepath
}

func sendKeyWithDelay(tm *teatest.TestModel, msg rune) {
	tm.Send(tea.KeyPressMsg{Code: msg})
	time.Sleep(time.Millisecond * millisecondDelay)
}

func sendModifiedKeyWithDelay(tm *teatest.TestModel, mod tea.KeyMod, msg rune) {
	tm.Send(tea.KeyPressMsg{Mod: mod, Code: msg})
	time.Sleep(time.Millisecond * millisecondDelay)
}

func typeWithDelay(tm *teatest.TestModel, s string) {
	for _, c := range s {
		tm.Send(tea.KeyPressMsg{
			Code: c,
			Text: string(c),
		})
		time.Sleep(time.Millisecond * millisecondDelay)
	}
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

func TestComplete(t *testing.T) {
	tm, filePath := setUpTUI(t)

	listToInput := `@ Verb
hear: audio, audire, audivi, auditus
take: capio, capere, cepi

@ Noun
girl: puella, puellae, (f)
farmer: agricola, agricolae, (m)
boy: puer, pueri, (m)
dog: canis, canis, (m)
name: nomen, nominis, (n)

@ Adjective
large: ingens, ingentis, (3-1)
light: levis, leve, (3-2)
keen: acer, acris, acre, (3-3)
good: bonus, bona, bonum, (212)
happy: laetus, laeta, laetum, (2-1-2)

@ Regular
into: in
from: e

@ Pronoun
this: hic, haec, hoc
that: ille`

	// Type out test input
	for line := range strings.SplitSeq(listToInput, "\n") {
		typeWithDelay(tm, line)
		time.Sleep(time.Millisecond * millisecondDelay)
		sendKeyWithDelay(tm, tea.KeyEnter)
		t.Logf("typed %s", line)
	}
	sendKeyWithDelay(tm, tea.KeyBackspace) // remove final line
	sendModifiedKeyWithDelay(tm, tea.ModCtrl, 's')

	// Test program output
	tm.WaitFinished(t, teatest.WithFinalTimeout(time.Second*3))
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)

	// Test vocab list output
	rawGot, err := os.ReadFile(filePath)
	if err != nil {
		t.Fatalf("error opening file %s: %s", filePath, err)
	}
	got := string(rawGot)
	assert.Equal(t, listToInput, got)
}
