module github.com/rduo1009/vocab-tuister

go 1.24

require (
	github.com/charmbracelet/bubbles/v2 v2.0.0-alpha.2
	github.com/charmbracelet/bubbletea/v2 v2.0.0-alpha.2
	github.com/charmbracelet/lipgloss/v2 v2.0.0-alpha.2
	github.com/elewis787/boa v0.1.2
	github.com/spf13/cobra v1.9.1
	github.com/widmogrod/mkunion v0.0.0-20220926122055-0884a4bef836
	golang.org/x/term v0.29.0
)

require (
	github.com/alecthomas/template v0.0.0-20190718012654-fb15b899a751 // indirect
	github.com/alecthomas/units v0.0.0-20231202071711-9a357b53e9c9 // indirect
	github.com/atotto/clipboard v0.1.4 // indirect
	github.com/aymanbagabas/go-osc52/v2 v2.0.1 // indirect
	github.com/aymanbagabas/go-udiff v0.2.0 // indirect
	github.com/bitfield/gotestdox v0.2.2 // indirect
	github.com/charmbracelet/bubbles v0.16.1 // indirect
	github.com/charmbracelet/bubbletea v0.24.2 // indirect
	github.com/charmbracelet/colorprofile v0.1.6 // indirect
	github.com/charmbracelet/lipgloss v0.7.1 // indirect
	github.com/charmbracelet/x/ansi v0.4.3 // indirect
	github.com/charmbracelet/x/cellbuf v0.0.3 // indirect
	github.com/charmbracelet/x/exp/golden v0.0.0-20241011142426-46044092ad91 // indirect
	github.com/charmbracelet/x/term v0.2.0 // indirect
	github.com/charmbracelet/x/wcwidth v0.0.0-20241011142426-46044092ad91 // indirect
	github.com/charmbracelet/x/windows v0.2.0 // indirect
	github.com/containerd/console v1.0.4-0.20230313162750-1ae8d489ac81 // indirect
	github.com/dave/dst v0.27.3 // indirect
	github.com/davecgh/go-spew v1.1.1 // indirect
	github.com/dmarkham/enumer v1.5.11 // indirect
	github.com/dnephin/pflag v1.0.7 // indirect
	github.com/fatih/color v1.16.0 // indirect
	github.com/fatih/structtag v1.2.0 // indirect
	github.com/fsnotify/fsnotify v1.7.0 // indirect
	github.com/google/go-cmp v0.6.0 // indirect
	github.com/google/shlex v0.0.0-20191202100458-e7afc7fbc510 // indirect
	github.com/hpcloud/tail v1.0.0 // indirect
	github.com/inconshreveable/mousetrap v1.1.0 // indirect
	github.com/lucasb-eyer/go-colorful v1.2.0 // indirect
	github.com/mattn/go-colorable v0.1.13 // indirect
	github.com/mattn/go-isatty v0.0.20 // indirect
	github.com/mattn/go-localereader v0.0.1 // indirect
	github.com/mattn/go-runewidth v0.0.16 // indirect
	github.com/mgutz/ansi v0.0.0-20200706080929-d51e80ef957d // indirect
	github.com/muesli/ansi v0.0.0-20230316100256-276c6243b2f6 // indirect
	github.com/muesli/cancelreader v0.2.2 // indirect
	github.com/muesli/reflow v0.3.0 // indirect
	github.com/muesli/termenv v0.15.2 // indirect
	github.com/niemeyer/pretty v0.0.0-20200227124842-a10e7caefd8e // indirect
	github.com/pascaldekloe/name v1.0.0 // indirect
	github.com/pmezard/go-difflib v1.0.0 // indirect
	github.com/rivo/uniseg v0.4.7 // indirect
	github.com/sahilm/fuzzy v0.1.1 // indirect
	github.com/sashabaranov/go-openai v1.26.3 // indirect
	github.com/segmentio/golines v0.12.2 // indirect
	github.com/sirupsen/logrus v1.9.3 // indirect
	github.com/spf13/pflag v1.0.6 // indirect
	github.com/x-cray/logrus-prefixed-formatter v0.5.2 // indirect
	github.com/xo/terminfo v0.0.0-20220910002029-abceb7e1c41e // indirect
	golang.org/x/crypto v0.33.0 // indirect
	golang.org/x/mod v0.23.0 // indirect
	golang.org/x/sync v0.11.0 // indirect
	golang.org/x/sys v0.30.0 // indirect
	golang.org/x/text v0.22.0 // indirect
	golang.org/x/tools v0.30.0 // indirect
	gopkg.in/alecthomas/kingpin.v2 v2.2.6 // indirect
	gopkg.in/check.v1 v1.0.0-20200227125254-8fa46927fb4f // indirect
	gopkg.in/fsnotify.v1 v1.4.7 // indirect
	gopkg.in/tomb.v1 v1.0.0-20141024135613-dd632973f1e7 // indirect
	gopkg.in/yaml.v3 v3.0.1 // indirect
	gotest.tools/gotestsum v1.12.0 // indirect
	mvdan.cc/gofumpt v0.7.0 // indirect
)

require (
	github.com/charmbracelet/x/exp/teatest/v2 v2.0.0-20250219214358-0881292cec0a // test
	github.com/stretchr/testify v1.9.0 // test
)

replace github.com/widmogrod/mkunion => ./src/_vendor/mkunion

tool (
	github.com/dmarkham/enumer
	github.com/segmentio/golines
	gotest.tools/gotestsum
	mvdan.cc/gofumpt
)
