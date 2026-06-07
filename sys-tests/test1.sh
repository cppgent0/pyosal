#! /usr/bin/env bash

pyexe="unset"
# shellcheck disable=SC1091
source tools/zpm_env quiet
export PYTHONPATH="."
$pyexe sys-tests/test1_timeout.py $@
rc=$?
echo "test1: rc=$rc"
