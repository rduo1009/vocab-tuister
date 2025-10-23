package cmd

import (
	"fmt"
	"os"

	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/spf13/cobra"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/root"
)

var rootCmd = &cobra.Command{
	Version: internal.Version,
	Use:     "vocab-tuister",
	Short:   "Latin vocabulary and grammar testing.",
	Long: `Vocab-tuister is a tool for improving your Latin vocabulary and endings.
The project homepage is at https://github.com/rduo1009/vocab-tuister.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		p := tea.NewProgram(root.New())
		if _, err := p.Run(); err != nil {
			return err
		}
		return nil
	},
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
