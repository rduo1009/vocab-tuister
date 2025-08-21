package sessiontui_test

import (
	"flag"
	"io"
	"net/http"
	"net/http/httptest"
	"net/url"
	"os"
	"path/filepath"
	"strconv"
	"testing"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
	"github.com/charmbracelet/x/exp/teatest"
	"github.com/muesli/termenv"

	"github.com/rduo1009/vocab-tuister/src/client/internal/sessiontui"
)

const (
	dummyConfigFilename = "dummy-config.json"
	dummyListFilename   = "dummy-list.txt"

	numberOfQuestions = 6

	millisecondDelay = 200
)

func init() {
	lipgloss.SetColorProfile(termenv.TrueColor)
}

func readBts(tb testing.TB, r io.Reader) []byte {
	tb.Helper()

	bts, err := io.ReadAll(r)
	if err != nil {
		tb.Fatal(err)
	}
	return bts
}

func setUpTUI(t *testing.T, port int) *teatest.TestModel {
	t.Helper()

	m := sessiontui.InitialModel(
		filepath.Join("testdata", dummyConfigFilename),
		filepath.Join("testdata", dummyListFilename),
		numberOfQuestions,
		port,
	)
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(300, 100))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})
	time.Sleep(time.Millisecond * millisecondDelay)

	return tm
}

func setUpMockServer(t *testing.T, sessionResponse string) (*httptest.Server, int) {
	t.Helper()

	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Path {
		case "/send-vocab":
			w.Header()
			w.WriteHeader(http.StatusOK)
			if _, err := w.Write([]byte("Vocab list received.")); err != nil {
				t.Fatalf("failed to write to send-vocab output: %v", err)
			}
		case "/session":
			w.Header().Set("Content-Type", "application/json")
			if _, err := w.Write([]byte(sessionResponse)); err != nil {
				t.Fatalf("failed to write to session output: %v", err)
			}
		default:
			http.Error(w, "not found", http.StatusNotFound)
		}
	}))

	u, err := url.Parse(server.URL)
	if err != nil {
		t.Fatalf("failed to parse test server URL: %v", err)
	}
	port, err := strconv.Atoi(u.Port())
	if err != nil {
		t.Fatalf("failed to extract port: %v", err)
	}

	return server, port
}

func sendKeyWithDelay(tm *teatest.TestModel, keyType tea.KeyType) {
	tm.Send(tea.KeyMsg{Type: keyType})
	time.Sleep(time.Millisecond * millisecondDelay)
}

func typeWithDelay(tm *teatest.TestModel, s string) {
	for _, c := range s {
		tm.Send(tea.KeyMsg{
			Type:  tea.KeyRunes,
			Runes: []rune{c},
		})
		time.Sleep(time.Millisecond * millisecondDelay)
	}
}

func answerMultipleChoiceOptionN(tm *teatest.TestModel, n int) {
	// Menu to option N (zero index)
	for range n {
		sendKeyWithDelay(tm, tea.KeyDown)
	}

	sendKeyWithDelay(tm, tea.KeyEnter) // Answer question
	tm.Type("abcdefg\n")               // Check if keys are locked
	sendKeyWithDelay(tm, tea.KeyEnter) // Next question
}

func answerText(tm *teatest.TestModel, ans string) {
	// Answer question
	typeWithDelay(tm, ans)
	sendKeyWithDelay(tm, tea.KeyEnter)
	tm.Type("abcdefg\n")               // Check if keys are locked
	sendKeyWithDelay(tm, tea.KeyEnter) // Next question
}

func answerPrincipalParts(tm *teatest.TestModel, ss []string) {
	// Answer question
	for _, s := range ss {
		typeWithDelay(tm, s)
		sendKeyWithDelay(tm, tea.KeyDown)
	}
	sendKeyWithDelay(tm, tea.KeyEnter)
	tm.Type("abcdefg\n")               // Check if keys are locked
	sendKeyWithDelay(tm, tea.KeyEnter) // Next question
}

func TestMain(m *testing.M) {
	flag.Parse()
	os.Exit(m.Run())
}

func TestMultipleChoiceEngtoLat(t *testing.T) {
	server, port := setUpMockServer(t, `[
{"question_type": "MultipleChoiceEngToLatQuestion", "MultipleChoiceEngToLatQuestion": {"prompt": "bar", "answer": "foo", "choices": ["foo", "bar", "baz"]}},
{"question_type": "MultipleChoiceEngToLatQuestion", "MultipleChoiceEngToLatQuestion": {"prompt": "bar", "answer": "foo", "choices": ["foo", "bar", "baz"]}},
{"question_type": "MultipleChoiceEngToLatQuestion", "MultipleChoiceEngToLatQuestion": {"prompt": "foo", "answer": "bar", "choices": ["baz", "bar", "qux"]}},
{"question_type": "MultipleChoiceEngToLatQuestion", "MultipleChoiceEngToLatQuestion": {"prompt": "foo", "answer": "bar", "choices": ["baz", "bar", "qux"]}},
{"question_type": "MultipleChoiceEngToLatQuestion", "MultipleChoiceEngToLatQuestion": {"prompt": "baz", "answer": "qux", "choices": ["bar", "foo", "qux"]}},
{"question_type": "MultipleChoiceEngToLatQuestion", "MultipleChoiceEngToLatQuestion": {"prompt": "baz", "answer": "qux", "choices": ["bar", "foo", "qux"]}}
	]`)
	defer server.Close()

	tm := setUpTUI(t, port)

	// Input commands to the TUI
	answerMultipleChoiceOptionN(tm, 0) // correct
	answerMultipleChoiceOptionN(tm, 1) // incorrect

	answerMultipleChoiceOptionN(tm, 1) // correct
	answerMultipleChoiceOptionN(tm, 2) // incorrect

	answerMultipleChoiceOptionN(tm, 2) // correct
	answerMultipleChoiceOptionN(tm, 0) // incorrect

	// Test program output
	tm.WaitFinished(t, teatest.WithFinalTimeout(time.Second*3))
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestMultipleChoiceLattoEng(t *testing.T) {
	server, port := setUpMockServer(t, `[
{"question_type": "MultipleChoiceLatToEngQuestion", "MultipleChoiceLatToEngQuestion": {"prompt": "bar", "answer": "foo", "choices": ["foo", "bar", "baz"]}},
{"question_type": "MultipleChoiceLatToEngQuestion", "MultipleChoiceLatToEngQuestion": {"prompt": "bar", "answer": "foo", "choices": ["foo", "bar", "baz"]}},
{"question_type": "MultipleChoiceLatToEngQuestion", "MultipleChoiceLatToEngQuestion": {"prompt": "foo", "answer": "bar", "choices": ["baz", "bar", "qux"]}},
{"question_type": "MultipleChoiceLatToEngQuestion", "MultipleChoiceLatToEngQuestion": {"prompt": "foo", "answer": "bar", "choices": ["baz", "bar", "qux"]}},
{"question_type": "MultipleChoiceLatToEngQuestion", "MultipleChoiceLatToEngQuestion": {"prompt": "baz", "answer": "qux", "choices": ["bar", "foo", "qux"]}},
{"question_type": "MultipleChoiceLatToEngQuestion", "MultipleChoiceLatToEngQuestion": {"prompt": "baz", "answer": "qux", "choices": ["bar", "foo", "qux"]}}
	]`)
	defer server.Close()

	tm := setUpTUI(t, port)

	// Input commands to the TUI
	answerMultipleChoiceOptionN(tm, 0) // correct
	answerMultipleChoiceOptionN(tm, 1) // incorrect

	answerMultipleChoiceOptionN(tm, 1) // correct
	answerMultipleChoiceOptionN(tm, 2) // incorrect

	answerMultipleChoiceOptionN(tm, 2) // correct
	answerMultipleChoiceOptionN(tm, 0) // incorrect

	// Test program output
	tm.WaitFinished(t, teatest.WithFinalTimeout(time.Second*3))
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestParseWordComptoLat(t *testing.T) {
	server, port := setUpMockServer(t, `[
{"question_type": "ParseWordCompToLatQuestion", "ParseWordCompToLatQuestion": {"prompt": "bar", "components": "quz", "main_answer": "foo", "answers": ["foo", "foofoo"]}},
{"question_type": "ParseWordCompToLatQuestion", "ParseWordCompToLatQuestion": {"prompt": "bar", "components": "quz", "main_answer": "foo", "answers": ["foo", "foofoo"]}},
{"question_type": "ParseWordCompToLatQuestion", "ParseWordCompToLatQuestion": {"prompt": "bar", "components": "quz", "main_answer": "foo", "answers": ["foo", "foofoo"]}},
{"question_type": "ParseWordCompToLatQuestion", "ParseWordCompToLatQuestion": {"prompt": "foo", "components": "quux", "main_answer": "bar", "answers": ["bar", "barbar"]}},
{"question_type": "ParseWordCompToLatQuestion", "ParseWordCompToLatQuestion": {"prompt": "foo", "components": "quux", "main_answer": "bar", "answers": ["bar", "barbar"]}},
{"question_type": "ParseWordCompToLatQuestion", "ParseWordCompToLatQuestion": {"prompt": "foo", "components": "quux", "main_answer": "bar", "answers": ["bar", "barbar"]}}
	]`)
	defer server.Close()

	tm := setUpTUI(t, port)

	// Input commands to the TUI
	answerText(tm, "foo")    // correct
	answerText(tm, "foofoo") // also correct
	answerText(tm, "bar")    // incorrect

	answerText(tm, "bar")    // correct
	answerText(tm, "barbar") // also correct
	answerText(tm, "baz")    // incorrect

	// Test program output
	tm.WaitFinished(t, teatest.WithFinalTimeout(time.Second*3))
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestParseWordLattoComp(t *testing.T) {
	server, port := setUpMockServer(t, `[
{"question_type": "ParseWordLatToCompQuestion", "ParseWordLatToCompQuestion": {"prompt": "bar", "dictionary_entry": "quz", "main_answer": "foo", "answers": ["foo", "foofoo"]}},
{"question_type": "ParseWordLatToCompQuestion", "ParseWordLatToCompQuestion": {"prompt": "bar", "dictionary_entry": "quz", "main_answer": "foo", "answers": ["foo", "foofoo"]}},
{"question_type": "ParseWordLatToCompQuestion", "ParseWordLatToCompQuestion": {"prompt": "bar", "dictionary_entry": "quz", "main_answer": "foo", "answers": ["foo", "foofoo"]}},
{"question_type": "ParseWordLatToCompQuestion", "ParseWordLatToCompQuestion": {"prompt": "foo", "dictionary_entry": "quux", "main_answer": "bar", "answers": ["bar", "barbar"]}},
{"question_type": "ParseWordLatToCompQuestion", "ParseWordLatToCompQuestion": {"prompt": "foo", "dictionary_entry": "quux", "main_answer": "bar", "answers": ["bar", "barbar"]}},
{"question_type": "ParseWordLatToCompQuestion", "ParseWordLatToCompQuestion": {"prompt": "foo", "dictionary_entry": "quux", "main_answer": "bar", "answers": ["bar", "barbar"]}}
	]`)
	defer server.Close()

	tm := setUpTUI(t, port)

	// Input commands to the TUI
	answerText(tm, "foo")    // correct
	answerText(tm, "foofoo") // also correct
	answerText(tm, "bar")    // incorrect

	answerText(tm, "bar")    // correct
	answerText(tm, "barbar") // also correct
	answerText(tm, "baz")    // incorrect

	// Test program output
	tm.WaitFinished(t, teatest.WithFinalTimeout(time.Second*3))
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestPrincipalParts(t *testing.T) {
	server, port := setUpMockServer(t, `[
{"question_type": "PrincipalPartsQuestion", "PrincipalPartsQuestion": {"prompt": "foo", "principal_parts": ["foo1", "foo2"]}},
{"question_type": "PrincipalPartsQuestion", "PrincipalPartsQuestion": {"prompt": "foo", "principal_parts": ["foo1", "foo2"]}},
{"question_type": "PrincipalPartsQuestion", "PrincipalPartsQuestion": {"prompt": "foo", "principal_parts": ["foo1", "foo2"]}},
{"question_type": "PrincipalPartsQuestion", "PrincipalPartsQuestion": {"prompt": "bar", "principal_parts": ["bar1", "bar2", "bar3"]}},
{"question_type": "PrincipalPartsQuestion", "PrincipalPartsQuestion": {"prompt": "bar", "principal_parts": ["bar1", "bar2", "bar3"]}},
{"question_type": "PrincipalPartsQuestion", "PrincipalPartsQuestion": {"prompt": "bar", "principal_parts": ["bar1", "bar2", "bar3"]}}
	]`)
	defer server.Close()

	tm := setUpTUI(t, port)

	// Input commands to the TUI
	answerPrincipalParts(tm, []string{"foo1", "foo2"}) // correct
	answerPrincipalParts(tm, []string{"foo1", "foo3"}) // one correct
	answerPrincipalParts(tm, []string{"foo3", "foo4"}) // all incorrect

	answerPrincipalParts(tm, []string{"bar1", "bar2", "bar3"}) // correct
	answerPrincipalParts(tm, []string{"bar0", "bar2", "bar3"}) // two correct
	answerPrincipalParts(tm, []string{"bar4", "bar5", "bar6"}) // all incorrect

	// Test program output
	tm.WaitFinished(t, teatest.WithFinalTimeout(time.Second*3))
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestTypeInEngtoLat(t *testing.T) {
	server, port := setUpMockServer(t, `[
{"question_type": "TypeInEngToLatQuestion", "TypeInEngToLatQuestion": {"prompt": "foo", "answers": ["baz", "bazbaz"], "main_answer": "baz"}},
{"question_type": "TypeInEngToLatQuestion", "TypeInEngToLatQuestion": {"prompt": "foo", "answers": ["baz", "bazbaz"], "main_answer": "baz"}},
{"question_type": "TypeInEngToLatQuestion", "TypeInEngToLatQuestion": {"prompt": "foo", "answers": ["baz", "bazbaz"], "main_answer": "baz"}},
{"question_type": "TypeInEngToLatQuestion", "TypeInEngToLatQuestion": {"prompt": "bar", "answers": ["qux", "quxqux"], "main_answer": "qux"}},
{"question_type": "TypeInEngToLatQuestion", "TypeInEngToLatQuestion": {"prompt": "bar", "answers": ["qux", "quxqux"], "main_answer": "qux"}},
{"question_type": "TypeInEngToLatQuestion", "TypeInEngToLatQuestion": {"prompt": "bar", "answers": ["qux", "quxqux"], "main_answer": "qux"}}
	]`)
	defer server.Close()

	tm := setUpTUI(t, port)

	// Input commands to the TUI
	answerText(tm, "baz")    // correct
	answerText(tm, "bazbaz") // also correct
	answerText(tm, "qux")    // incorrect

	answerText(tm, "qux")    // correct
	answerText(tm, "quxqux") // also correct
	answerText(tm, "baz")    // incorrect

	// Test program output
	tm.WaitFinished(t, teatest.WithFinalTimeout(time.Second*3))
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}

func TestTypeInLattoEng(t *testing.T) {
	server, port := setUpMockServer(t, `[
{"question_type": "TypeInLatToEngQuestion", "TypeInLatToEngQuestion": {"prompt": "foo", "answers": ["baz", "bazbaz"], "main_answer": "baz"}},
{"question_type": "TypeInLatToEngQuestion", "TypeInLatToEngQuestion": {"prompt": "foo", "answers": ["baz", "bazbaz"], "main_answer": "baz"}},
{"question_type": "TypeInLatToEngQuestion", "TypeInLatToEngQuestion": {"prompt": "foo", "answers": ["baz", "bazbaz"], "main_answer": "baz"}},
{"question_type": "TypeInLatToEngQuestion", "TypeInLatToEngQuestion": {"prompt": "bar", "answers": ["qux", "quxqux"], "main_answer": "qux"}},
{"question_type": "TypeInLatToEngQuestion", "TypeInLatToEngQuestion": {"prompt": "bar", "answers": ["qux", "quxqux"], "main_answer": "qux"}},
{"question_type": "TypeInLatToEngQuestion", "TypeInLatToEngQuestion": {"prompt": "bar", "answers": ["qux", "quxqux"], "main_answer": "qux"}}
	]`)
	defer server.Close()

	tm := setUpTUI(t, port)

	// Input commands to the TUI
	answerText(tm, "baz")    // correct
	answerText(tm, "bazbaz") // also correct
	answerText(tm, "qux")    // incorrect

	answerText(tm, "qux")    // correct
	answerText(tm, "quxqux") // also correct
	answerText(tm, "baz")    // incorrect

	// Test program output
	tm.WaitFinished(t, teatest.WithFinalTimeout(time.Second*3))
	out := readBts(t, tm.FinalOutput(t))
	teatest.RequireEqualOutput(t, out)
}
