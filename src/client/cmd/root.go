package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
)

var rootCmd = &cobra.Command{
	Version: internal.Version,
	Use:     "vocab-tuister",
	Short:   "Latin vocabulary and grammar testing.",
	Long: `Vocab-tuister is a tool for improving your Latin vocabulary and endings.
The project homepage is at https://github.com/rduo1009/vocab-tuister.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		if len(args) == 0 {
			if err := cmd.Help(); err != nil {
				return err
			}
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
