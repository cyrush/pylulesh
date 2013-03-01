#!/bin/sh
set -x

function build
{
    if [[ -e tests/target_test_kernel1-c ]]
    then
        return 0
    fi
    python ./libs/pypy-pypy/pypy//translator/goal/translate.py tests/target_test_kernel1.py
    mv target_test_kernel1-c tests/
}

function runtest
{
    for dim in 5 25 50
    do
        time python tests/target_test_kernel1.py $dim
        time ./tests/target_test_kernel1-c $dim
    done
}

build
runtest
