#!/bin/bash

mkdir -p reports/coverage

echo -n "Running Python tests with coverage... "
poetry run coverage run -m pytest -m 'not integration and not manual' -n0 >> /dev/null
poetry run coverage run -m pytest -m 'integration' -n0 >> /dev/null
poetry run coverage combine --append >> /dev/null
echo "done"

echo -n "Running Go tests with coverage... "
go test -covermode=atomic -coverprofile=reports/coverage/coverage.out ./src/... >> /dev/null
./tests/integration/client_integration/client-integration-tests.sh
echo "done"

echo -n "Generating coverage reports... "
poetry run coverage html >> /dev/null
poetry run coverage xml -o reports/coverage/coverage.xml >> /dev/null
echo "done"
