#!/bin/sh
set -x

export PYTHONPATH=$PWD/src:$PYTHONPATH

function build
{
    if [[ -e pypy-tests/target_test_kernel1-c ]]
    then
        return 0
    fi
    python ./libs/pypy-pypy/pypy//translator/goal/translate.py pypy-tests/target_test_kernel1.py
    mv target_test_kernel1-c pypy-tests/
}

function runtest
{
    for dim in 5 25 50
    do
        time python pypy-tests/target_test_kernel1.py $dim
        time ./pypy-tests/target_test_kernel1-c $dim
    done
}

build || exit 1
runtest || exit 1
