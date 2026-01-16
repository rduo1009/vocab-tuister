#!/bin/bash

set -e

echo "🚀 Setting up Vocab Tuister development environment..."

# Update package list
sudo apt-get update

# Install uv
echo "⚡ Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Install Python dependencies with uv
echo "🐍 Installing Python dependencies..."
uv sync

# Install pre-commit
echo "🔧 Installing pre-commit..."
uv tool install pre-commit

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install

# Install golangci-lint
echo "🐹 Installing golangci-lint..."
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v1.62.2

# Install Go modules and tools
echo "📋 Installing Go modules and tools..."
go mod tidy
go mod download

# Install Go tools specified in go.mod
echo "🔨 Installing Go tools..."
go install github.com/charmbracelet/vhs@latest
go install github.com/segmentio/golines@latest
go install mvdan.cc/gofumpt@latest
go install gotest.tools/gotestsum@latest
go install github.com/wadey/gocovmerge@latest

# Run go generate to set up code generation
echo "⚡ Running go generate..."
go generate -x src/generate.go

# Verify installations
echo "✅ Verifying installations..."
echo "Python: $(python --version)"
echo "uv: $(uv --version)"
echo "Go: $(go version)"
echo "golangci-lint: $(golangci-lint --version)"
echo "pre-commit: $(pre-commit --version)"
echo "GitHub CLI: $(gh --version)"

echo "🎉 Development environment setup complete!"
echo "📖 You can now run 'uv run <command>' to run commands in the environment"
echo "🧪 Run tests with 'uv run pytest' or 'go test ./...' for Go tests"
echo "🔍 Run linters with 'pre-commit run --all-files'"