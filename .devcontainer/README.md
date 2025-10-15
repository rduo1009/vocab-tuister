# Devcontainer Configuration

This directory contains the development container configuration for the Vocab Tuister project.

## What's Included

The devcontainer provides a complete development environment with:

### Languages & Runtimes

- **Python 3.14** - Required for the vocab-tuister server
- **Go 1.25** - Required for the vocab-tuister client

### Development Tools

- **Poetry** - Python dependency management and virtual environments
- **pipx** - Python application installer
- **pre-commit** - Git hooks for code quality
- **golangci-lint** - Go linter and code analyzer
- **GitHub CLI** - GitHub command line interface
- **Git** - Version control

### VS Code Extensions

- Python support with debugging, type checking, and formatting
- Go language support
- TOML, YAML editing support
- Error highlighting and todo highlighting
- Ruff formatter and linter integration

## Getting Started

1. **Open in Dev Container**: Click the "Reopen in Container" prompt in VS Code, or run the "Dev Containers: Reopen in Container" command from the Command Palette.

1. **Wait for Setup**: The first time you open the container, it will automatically run the setup script which:

   - Installs all required tools
   - Sets up Poetry virtual environment
   - Installs Python and Go dependencies
   - Configures pre-commit hooks
   - Installs Go tools

1. **Start Developing**: Once setup is complete, you can:

   - Activate the Python virtual environment: `poetry shell`
   - Run Python tests: `poetry run pytest`
   - Run Go tests: `go test ./...`
   - Run linters: `pre-commit run --all-files`
   - Build the project: `./scripts/build.sh`

## Configuration

The devcontainer is configured to:

- Mount a persistent volume for Poetry cache
- Forward ports 5000 and 8080 for local development
- Set up the Python virtual environment in the project directory
- Configure VS Code settings for optimal development experience

## Troubleshooting

If you encounter issues:

1. **Rebuild the container**: Use "Dev Containers: Rebuild Container" from the Command Palette
1. **Check setup logs**: Look at the output from the setup script during container creation
1. **Manual setup**: If automatic setup fails, you can run `.devcontainer/setup.sh` manually

## Dependencies Updates

The devcontainer image and its dependencies are automatically updated weekly via Dependabot.
