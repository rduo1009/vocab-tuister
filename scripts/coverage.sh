#!/bin/bash

mkdir -p reports/coverage

echo -n "Running Python tests with coverage... "
poetry run coverage run -m pytest -m 'not integration and not manual' -n0
poetry run coverage run -m pytest -m 'integration' -n0
poetry run coverage combine --append
echo "done"

echo -n "Running Go tests with coverage... "
go test -covermode=atomic -coverprofile=reports/coverage/gocoverage.out ./src/...
./tests/integration/client_integration/client-integration-tests.sh
echo "done"

echo -n "Generating coverage reports... "
poetry run coverage html
poetry run coverage xml -o reports/coverage/pycoverage.xml
go tool covdata textfmt -i=gocov -o=reports/coverage/gocoverage-integration.out
echo "done"
