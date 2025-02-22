#!/bin/bash

echo -n "Running tests with coverage... "
coverage run -m pytest -m 'not integration and not manual' -n0 >> /dev/null
coverage run -m pytest -m 'integration' -n0 >> /dev/null
coverage combine --append >> /dev/null
echo "done"

echo -n "Generating coverage reports... "
coverage html >> /dev/null
mkdir -p reports/coverage
coverage xml -o reports/coverage/coverage.xml >> /dev/null
echo "done"
