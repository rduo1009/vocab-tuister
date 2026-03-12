package cmd

import (
	"bytes"
	"embed"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"net"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
	"time"

	tea "charm.land/bubbletea/v2"
	"charm.land/huh/v2/spinner"
	"github.com/spf13/cobra"

	"github.com/rduo1009/vocab-tuister/src/assets"
	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/root"
)

var (
	serverPort int
	noServer   bool
	debugMode  bool
)

// getServerBinaryNames returns a list of possible server binary names based on the current platform and architecture.
// It follows the naming convention used in the build process (vocab-tuister-server.spec).
func getServerBinaryNames() []string {
	osName := runtime.GOOS
	arch := runtime.GOARCH

	// Normalise architecture names to match the ones used in the server build
	normalizedArch := arch
	switch arch {
	case "amd64":
		normalizedArch = "x86_64"

	case "arm64":
		if osName == "linux" {
			normalizedArch = "aarch64"
		} else {
			normalizedArch = "arm64"
		}
	}

	baseName := fmt.Sprintf("vocab-tuister-server-%s-%s", osName, normalizedArch)
	if osName == "windows" {
		baseName += ".exe"
	}
	names := []string{baseName}

	// On macOS, we also check for the universal2 binary as it is the default build target in CI
	if osName == "darwin" {
		names = append(names, "vocab-tuister-server-darwin-universal2")
	}

	return names
}

// startServer starts the vocab-tuister server in the background.
// If debug is true, it uses 'python3 -m src'.
// Otherwise, it looks for the pre-built binary in the executable's directory or on the PATH.
func startServer(debug bool, port int, stdout, stderr io.Writer) (*exec.Cmd, error) {
	var cmd *exec.Cmd

	if debug {
		// In debug mode, run the server using the python module
		cmd = exec.Command("python3", "-m", "src", "-p", strconv.Itoa(port))
	} else {
		// In production mode, look for the compiled binary
		binaryNames := getServerBinaryNames()

		var fullPath string

		for _, name := range binaryNames {
			// First, check the directory where the current client binary is located
			if exePath, err := os.Executable(); err == nil {
				localPath := filepath.Join(filepath.Dir(exePath), name)
				if _, err := os.Stat(localPath); err == nil {
					fullPath = localPath
					break
				}
			}

			// Second, check the system PATH
			if p, err := exec.LookPath(name); err == nil {
				fullPath = p
				break
			}
		}

		if fullPath == "" {
			return nil, fmt.Errorf("failed to find server binary (tried %v)", binaryNames)
		}

		cmd = exec.Command(fullPath, "-p", strconv.Itoa(port))
	}

	cmd.Stdout = stdout
	cmd.Stderr = stderr

	// Start the server in the background
	if err := cmd.Start(); err != nil {
		return nil, fmt.Errorf("failed to start server process: %w", err)
	}

	return cmd, nil
}

func isPortInUse(port int) bool {
	address := fmt.Sprintf("127.0.0.1:%d", port)

	ln, err := net.Listen("tcp", address)
	if err != nil {
		return true
	}

	_ = ln.Close()

	return false
}

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
	Version:      internal.Version,
	Use:          "vocab-tuister",
	Short:        "Latin vocabulary and grammar testing.",
	SilenceUsage: true,
	Long: `Vocab-tuister is a tool for improving your Latin vocabulary and endings.
The project homepage is at https://github.com/rduo1009/vocab-tuister.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		if !noServer {
			if isPortInUse(serverPort) {
				return fmt.Errorf("port %d is already in use; the server cannot start", serverPort)
			}

			// cyclopts errors printed to stdout, normal errors printed to stderr
			var (
				outBuf bytes.Buffer
				errBuf bytes.Buffer
			)

			serverCmd, err := startServer(debugMode, serverPort, &outBuf, &errBuf)
			if err != nil {
				return fmt.Errorf("failed to start server: %w", err)
			}

			defer func() {
				if serverCmd != nil && serverCmd.Process != nil {
					_ = serverCmd.Process.Signal(os.Interrupt)
					_, _ = serverCmd.Process.Wait()
				}
			}()

			errCh := make(chan error, 1)

			go func() {
				errCh <- serverCmd.Wait()
			}()

			var startupErr error

			spinErr := spinner.New().
				Title(fmt.Sprintf("Server starting on PID %d and port %d...", serverCmd.Process.Pid, serverPort)).
				Action(func() {
					ticker := time.NewTicker(200 * time.Millisecond)
					defer ticker.Stop()

					timeout := time.After(15 * time.Second)

					for {
						select {
						case err := <-errCh:
							outStr := strings.TrimSpace(outBuf.String())
							errStr := strings.TrimSpace(errBuf.String())

							var msg string
							if err != nil {
								msg = fmt.Sprintf("server exited unexpectedly: %v", err)
							} else {
								msg = "server exited unexpectedly (status 0)"
							}

							if outStr != "" {
								msg += "\nstdout:\n" + outStr
							}

							if errStr != "" {
								msg += "\nstderr:\n" + errStr
							}

							startupErr = fmt.Errorf("%s", msg)

							return

						case <-timeout:
							startupErr = errors.New("timed out waiting for server to start")
							return

						case <-ticker.C:
							resp, err := http.Get(
								fmt.Sprintf("http://127.0.0.1:%d/health", serverPort),
							)
							if err == nil {
								resp.Body.Close()

								if resp.StatusCode == http.StatusOK {
									return
								}
							}
						}
					}
				}).
				Run()
			if spinErr != nil {
				return fmt.Errorf("spinner error: %w", spinErr)
			}

			if startupErr != nil {
				return startupErr
			}
		}

		// XXX: https://github.com/charmbracelet/bubbles/pull/776 would remove need for this
		inbuiltListTmpDir, err := os.MkdirTemp("", "inbuilt-lists")
		if err != nil {
			return err
		}
		defer os.RemoveAll(inbuiltListTmpDir)

		if err := extractEmbeddedFS(assets.InbuiltLists, inbuiltListTmpDir); err != nil {
			return err
		}

		p := tea.NewProgram(root.New(inbuiltListTmpDir, serverPort))
		if _, err := p.Run(); err != nil {
			return err
		}

		return nil
	},
}

func Execute() {
	rootCmd.PersistentFlags().IntVarP(&serverPort, "port", "p", 5500, "port to run server on")
	rootCmd.PersistentFlags().BoolVar(&noServer, "no-server", false, "do not start server - TUI only")
	rootCmd.PersistentFlags().BoolVar(&debugMode, "debug", false, "enable debug mode")

	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}
