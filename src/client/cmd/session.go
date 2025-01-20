package cmd

import (
	"fmt"
	"os"

	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/spf13/cobra"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/rduo1009/vocab-tuister/src/client/internal/sessiontui"
)

var (
	sessionConfigPath string
	vocabListPath     string
	numberOfQuestions int
	serverPort        int
)

var sessionCmd = &cobra.Command{
	Version: internal.Version,
	Use:     "session",
	Short:   "Starts a testing session.",
	Long: `Starts a testing session.
This is based on the vocab list and the session config file provided.`,
	Run: func(cmd *cobra.Command, args []string) { //nolint:revive
		if sessionConfigPath == "" {
			fmt.Println("Error: --session-config is required.")
			os.Exit(1)
		}

		if vocabListPath == "" {
			fmt.Println("Error: --vocab-list is required.")
			os.Exit(1)
		}

		if numberOfQuestions <= 0 {
			fmt.Println("Error: --number must be a positive integer.")
			os.Exit(1)
		}

		if serverPort < 1 || serverPort > 65535 {
			fmt.Println("Error: --server-port must be a valid port number between 1 and 65535.")
			os.Exit(1)
		}

		p := tea.NewProgram(sessiontui.InitialModel(sessionConfigPath, vocabListPath, numberOfQuestions, serverPort))
		if _, err := p.Run(); err != nil {
			fmt.Println(err)
			os.Exit(1)
		}
	},
}

func init() {
	rootCmd.AddCommand(sessionCmd)

	sessionCmd.Flags().StringVarP(&sessionConfigPath, "session-config", "c", "", "Path to the session config .json file")
	sessionCmd.Flags().StringVarP(&vocabListPath, "vocab-list", "l", "", "Path to the vocab list .txt file")
	sessionCmd.Flags().IntVarP(&numberOfQuestions, "number", "n", 0, "Number of questions for the session")
	sessionCmd.Flags().IntVarP(&serverPort, "server-port", "p", 5000, "Localhost port for the server (default is 5000)")

	sessionCmd.MarkFlagRequired("session-config") //nolint:errcheck
	sessionCmd.MarkFlagRequired("vocab-list")     //nolint:errcheck
	sessionCmd.MarkFlagRequired("number")         //nolint:errcheck
}
