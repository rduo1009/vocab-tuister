#!/bin/bash

coverage run tests/run_all_tests.py 
mkdir -p reports/coverage 
coverage xml -o reports/coverage/pycoverage.xml 
genbadge coverage -o docs/assets/coverage-badge.svg

interrogate -v src -c setup.cfg --generate-badge docs/assets --quiet
