from __future__ import print_function

import subprocess
import sys

# this script execute tier testsing for pylero
# if the first argument is "tier0" it tests tier0
# if the first argument is "tier1" it tests tier1
# if the first argument is 'all' it  tests tier0+tier1


def get_command(x):
    return {
        "tier0": "attribute_test",
        "tier1": "test_run_test document_test work_item_test plan_test",
        "all": "attribute_test test_run_test document_test" " work_item_test plan_test",
    }.get(x)


if __name__ == "__main__":
    nose = "nose2 --plugin nose2.plugins.junitxml --junit-xml"
    coverage = " --with-coverage --coverage-report xml"
    src = " -s src/unit_tests "
    tests = None

    if len(sys.argv) == 2:
        tests = get_command(sys.argv[1])

    if tests:
        command = nose + coverage + src + tests
        print("Execute " + tests + ":")
        sys.exit(subprocess.call(command.split()))
    else:
        print("Usage: tiertests.py [args]")
        print("args: 'tier0' or 'tier1' or 'all'")
        sys.exit(1)
