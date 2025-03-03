#!/bin/bash

set -e
export PATH="$(pwd):$PATH"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

go build \
    -ldflags "-X github.com/rduo1009/vocab-tuister/src/client/internal.Version=$(dunamai from any)" \
    -cover \
    -o ./vocab-tuister \
    ./src

mkdir -p reports/coverage/go-integration

for tape in "$SCRIPT_DIR/"*.tape; do
    go tool vhs "$tape"
done

rm ./vocab-tuister

if git status --porcelain | grep -q .; then
    echo "Some tests failed:"
    git status
    exit 1
else
    echo "All tests passed."
fi