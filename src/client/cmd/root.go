package cmd

import (
	"embed"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"

	tea "charm.land/bubbletea/v2"
	"github.com/spf13/cobra"

	"github.com/rduo1009/vocab-tuister/src/assets"
	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/root"
)

func extractEmbeddedFS(efs embed.FS, target string) error {
	return fs.WalkDir(efs, ".", func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}

		if d.IsDir() {
			return nil
		}

		data, err := efs.ReadFile(path)
		if err != nil {
			return err
		}

		dst := filepath.Join(target, path)
		if err := os.MkdirAll(filepath.Dir(dst), 0o755); err != nil {
			return err
		}

		return os.WriteFile(dst, data, 0o644)
	})
}

var rootCmd = &cobra.Command{
	Version: internal.Version,
	Use:     "vocab-tuister",
	Short:   "Latin vocabulary and grammar testing.",
	Long: `Vocab-tuister is a tool for improving your Latin vocabulary and endings.
The project homepage is at https://github.com/rduo1009/vocab-tuister.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		// XXX: https://github.com/charmbracelet/bubbles/pull/776 would remove need for this
		inbuiltListTmpDir, err := os.MkdirTemp("", "inbuilt-lists")
		if err != nil {
			return err
		}

		if err := extractEmbeddedFS(assets.InbuiltLists, inbuiltListTmpDir); err != nil {
			return err
		}

		p := tea.NewProgram(root.New(inbuiltListTmpDir))
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
