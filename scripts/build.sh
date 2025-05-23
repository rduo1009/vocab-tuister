#!/bin/bash

set -e

if [[ $debug == "True" ]]; then
    echo "====== DEBUG MODE ======"
fi

# Only install necessary deps to speed up build
# poetry install --only main --sync # slower
poetry env remove --all
poetry install --only main

# Install deps that need to be in universal2
if [[ "$target_arch" == "universal2" ]]; then
    if [[ "$(uname)" == "Darwin" ]]; then
        python3 -m pip install --force https://files.pythonhosted.org/packages/90/73/bcb0e36614601016552fa9344544a3a2ae1809dc1401b100eab02e772e1f/regex-2024.11.6-cp313-cp313-macosx_10_13_universal2.whl
        python3 -m pip install --force https://files.pythonhosted.org/packages/83/0e/67eb10a7ecc77a0c2bbe2b0235765b98d164d81600746914bebada795e97/MarkupSafe-3.0.2-cp313-cp313-macosx_10_13_universal2.whl
        python3 -m pip install --force src/_build/macos/wheels/*.whl
    fi
fi

# Build
dunamai from any > __version__.txt
if [[ -z "$target_arch" ]]; then
    if [[ $debug == "True" ]]; then
        pyinstaller vocab-tuister-server.spec -- --debug
    else
        pyinstaller vocab-tuister-server.spec
    fi
else
    if [[ $debug == "True" ]]; then
        pyinstaller vocab-tuister-server.spec -- --debug --target-arch "$target_arch"
    else
        pyinstaller vocab-tuister-server.spec -- --target-arch "$target_arch"
    fi
fi

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
            clientbin_name="windows"
            ;;
        *)
            echo "Unknown OS"
            exit 1
            ;;
    esac
fi

go mod tidy
go generate -x src/generate.go
if [[ "$build_universal2" == "true" ]]; then
    tmpdir=$(mktemp -d)
    version=$(dunamai from any)

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
        -ldflags "-X github.com/rduo1009/vocab-tuister/src/client/internal.Version=$(dunamai from any)" \
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