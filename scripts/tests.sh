#!/bin/bash

uv run pytest -m 'not manual and not integration'
go test ./...