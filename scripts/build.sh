#!/bin/bash
set -e

# Set GOEXPERIMENT for encoding/json/v2
export GOEXPERIMENT=jsonv2

# CI is set to "true" automatically by GitHub Actions
CI="${CI:-false}"

mkdir -p dist

# Check generated files are up to date
poe generate
status="$(git status --porcelain)"
if [[ -n "$status" ]]; then
	echo >&2 "Error: Code changes after poe generate."
	echo >&2 "$status"
	exit 1
fi

# Determine binary name
case "$(uname -s)" in
Darwin)
	arch=$(uname -m)
	if [[ "$arch" == "arm64" ]]; then
		binary_name="darwin-arm64"
	else
		binary_name="darwin-x86_64"
	fi
	;;
Linux)
	arch=$(uname -m)
	if [[ "$arch" == "aarch64" ]]; then
		binary_name="linux-aarch64"
	else
		binary_name="linux-x86_64"
	fi
	;;
MINGW* | CYGWIN* | MSYS*)
	arch=$(uname -m)
	if [[ "$arch" == "aarch64" || "$arch" == "arm64" ]]; then
		binary_name="windows-arm64"
	else
		binary_name="windows-x86_64"
	fi
	;;
*)
	echo "Unknown OS" >&2
	exit 1
	;;
esac

# Add Windows .exe extension for output files
if [[ "$(uname -s)" == MINGW* || "$(uname -s)" == MSYS* || "$(uname -s)" == CYGWIN* ]]; then
	server_output_file="./dist/vocab-tuister-server-${binary_name}.exe"
	client_output_file="./dist/vocab-tuister-${binary_name}.exe"
else
	server_output_file="./dist/vocab-tuister-server-${binary_name}"
	client_output_file="./dist/vocab-tuister-${binary_name}"
fi

# Build python server
uv venv --allow-existing
uv sync --no-group=types --no-dev
uv run dunamai from any --style=semver >__version__.txt

nuitka_args=(src --output-filename="$server_output_file")
if [ "$CI" = "true" ]; then
	nuitka_args+=(--assume-yes-for-downloads --deployment)
fi
uv run nuitka "${nuitka_args[@]}"

# Build go client
version=$(uv run dunamai from any --style=semver)
go build \
	-ldflags "-X github.com/rduo1009/vocab-tuister/src/client/internal.Version=$version" \
	-o "$client_output_file" \
	./src/main.go
