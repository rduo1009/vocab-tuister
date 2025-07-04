#!/bin/bash

set -e

if [[ $debug == "True" ]]; then
    echo "====== DEBUG MODE ======"
fi

# Only install necessary deps to speed up build
# poetry sync --only main # slower
poetry env remove --all
poetry install --only main

# Install deps that need to be in universal2
if [[ "$target_arch" == "universal2" ]]; then
    if [[ "$(uname)" == "Darwin" ]]; then
        poetry run python3 -m pip install --force https://files.pythonhosted.org/packages/90/73/bcb0e36614601016552fa9344544a3a2ae1809dc1401b100eab02e772e1f/regex-2024.11.6-cp313-cp313-macosx_10_13_universal2.whl
        poetry run python3 -m pip install --force https://files.pythonhosted.org/packages/83/0e/67eb10a7ecc77a0c2bbe2b0235765b98d164d81600746914bebada795e97/MarkupSafe-3.0.2-cp313-cp313-macosx_10_13_universal2.whl
        poetry run python3 -m pip install --force src/_build/macos/wheels/*.whl
    fi
fi

# Build python server
poetry run dunamai from any > __version__.txt
if [[ -z "$target_arch" ]]; then
    if [[ $debug == "True" ]]; then
        poetry run pyinstaller vocab-tuister-server.spec -- --debug
    else
        poetry run pyinstaller vocab-tuister-server.spec
    fi
else
    if [[ $debug == "True" ]]; then
        poetry run pyinstaller vocab-tuister-server.spec -- --debug --target-arch "$target_arch"
    else
        poetry run pyinstaller vocab-tuister-server.spec -- --target-arch "$target_arch"
    fi
fi

# Determine client binary name
if [[ -n "$target_arch" ]]; then
    if [[ "$target_arch" == "universal2" ]]; then
        clientbin_name="darwin-universal2"
        build_universal2=true
    else
        clientbin_name="darwin-$target_arch"
    fi
else
    case "$(uname -s)" in
        Darwin)
            arch=$(uname -m)
            if [[ "$arch" == "arm64" ]]; then
                clientbin_name="darwin-arm64"
            else
                clientbin_name="darwin-x86_64"
            fi
            ;;
        Linux)
            arch=$(uname -m)
            if [[ "$arch" == "aarch64" ]]; then
                clientbin_name="linux-aarch64"
            else
                clientbin_name="linux-x86_64"
            fi
            ;;
        MINGW*|CYGWIN*|MSYS*)
            arch=$(uname -m)
            if [[ "$arch" == "aarch64" || "$arch" == "arm64" ]]; then
                clientbin_name="windows-arm64"
            else
                clientbin_name="windows-x86_64"
            fi
            ;;
        *)
            echo "Unknown OS"
            exit 1
            ;;
    esac
fi

# Add Windows .exe extension for the output file
if [[ "$(uname -s)" == MINGW* || "$(uname -s)" == MSYS* || "$(uname -s)" == CYGWIN* ]]; then
    output_file="./dist/vocab-tuister-${clientbin_name}.exe"
else
    output_file="./dist/vocab-tuister-${clientbin_name}"
fi

# Build go client
go mod tidy
go generate -x ./... && git diff --quiet || { echo >&2 "Error: Code changes after go generate."; exit 1; }

version=$(poetry run dunamai from any)
if [[ "$build_universal2" == "true" ]]; then
    tmpdir=$(mktemp -d)

    GOOS=darwin GOARCH=arm64 go build \
        -o "$tmpdir/arm64" \
        -ldflags "-X github.com/rduo1009/vocab-tuister/src/client/internal.Version=$version" \
        ./src/main.go

    GOOS=darwin GOARCH=amd64 go build \
        -o "$tmpdir/amd64" \
        -ldflags "-X github.com/rduo1009/vocab-tuister/src/client/internal.Version=$version" \
        ./src/main.go

    lipo -create "$tmpdir/arm64" "$tmpdir/amd64" -o "./dist/vocab-tuister-$clientbin_name"

    rm -r "$tmpdir"
else
    go build \
        -ldflags "-X github.com/rduo1009/vocab-tuister/src/client/internal.Version=$version" \
        -o "./dist/vocab-tuister-$clientbin_name" \
        ./src/main.go
fi

# echo -n "Do you want to reinstall all deps? (Y/n) "
# read -r response
# echo
# if [[ -z "$response" || "$response" == "y" || "$response" == "Y" ]]; then
#     poetry install --sync
# else
#     poetry install --only main --sync
# fi