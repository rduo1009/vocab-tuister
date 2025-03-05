#!/bin/bash

mkdir -p reports/coverage

echo -n "Running Python tests with coverage... "
poetry run coverage run -m pytest -m 'not integration and not manual' -n0
poetry run coverage run -m pytest -m 'integration' -n0
poetry run coverage combine --append
echo "done"

echo -n "Running Go tests with coverage... "
go test -coverprofile=reports/coverage/go-unit.out ./src/...
./tests/integration/client_integration/client-integration-tests.sh
echo "done"

echo -n "Generating coverage reports... "
poetry run coverage html
poetry run coverage xml -o reports/coverage/pycoverage.xml
go tool covdata textfmt -i=reports/coverage/go-integration -o=reports/coverage/go-integration.out
go tool gocovmerge reports/coverage/go-integration.out reports/coverage/go-unit.out > reports/coverage/go-combined.out
echo "done"
