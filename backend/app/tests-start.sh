#! /usr/bin/env bash
set -e

python ./app/tests_pre_start.py

pytest $* ./app/tests/
