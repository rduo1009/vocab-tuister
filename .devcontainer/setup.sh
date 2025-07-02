#!/bin/bash

set -e

echo "🚀 Setting up Vocab Tuister development environment..."

# Update package list
sudo apt-get update

# Install pipx
echo "📦 Installing pipx..."
sudo apt-get install -y pipx
pipx ensurepath

# Install poetry using pipx
echo "📝 Installing Poetry..."
pipx install poetry

# Configure poetry
echo "⚙️  Configuring Poetry..."
poetry config virtualenvs.create true
poetry config virtualenvs.in-project true

# Install Python dependencies with poetry
echo "🐍 Installing Python dependencies..."
poetry install --sync

# Install pre-commit
echo "🔧 Installing pre-commit..."
pipx install pre-commit

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
echo "Poetry: $(poetry --version)"
echo "Go: $(go version)"
echo "golangci-lint: $(golangci-lint --version)"
echo "pre-commit: $(pre-commit --version)"
echo "GitHub CLI: $(gh --version)"

echo "🎉 Development environment setup complete!"
echo "📖 You can now run 'poetry shell' to activate the virtual environment"
echo "🧪 Run tests with 'poetry run pytest' or 'go test ./...' for Go tests"
echo "🔍 Run linters with 'pre-commit run --all-files'"