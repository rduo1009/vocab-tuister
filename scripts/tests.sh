#!/bin/bash

uv run pytest -m 'not manual and not integration'
NERD_FONTS=0 go test ./...
