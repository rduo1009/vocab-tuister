package cmd

import (
	"fmt"
	"os"

	"github.com/elewis787/boa"
	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/spf13/cobra"
)

var version string = internal.Version

var rootCmd = &cobra.Command{
	Version: version,
	Use:     "vocab-tuister",
	Short:   "Latin vocabulary and grammar testing.",
	Long: `Vocab-tuister is a tool for improving your Latin vocabulary and endings.
The project homepage is at https://github.com/rduo1009/vocab-tuister.`,
	Run: func(cmd *cobra.Command, args []string) {
		if len(args) == 0 {
			if err := cmd.Help(); err != nil {
				fmt.Fprintln(os.Stderr, err)
			}
			os.Exit(0)
		}
	},
}

func Execute() {
	rootCmd.SetUsageFunc(boa.UsageFunc)
	rootCmd.SetHelpFunc(boa.HelpFunc)

	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
