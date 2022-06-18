from typing import Sequence

from ..common import AssessedStudent, check_empty_args


def report_markdown_basic(
    assessed_students: Sequence[AssessedStudent], args: Sequence[str]
):
    """Generate a basic Markdown assessment report."""

    # args should be empty
    check_empty_args(args)

    print("This is the markdown basic report plugin")
    print(assessed_students)


def report_stdout_basic(
    assessed_students: Sequence[AssessedStudent], args: Sequence[str]
):
    """Generate a basic assessment report directly to the standard output."""

    # args should be empty
    check_empty_args(args)

    print("This is the stdout basic report plugin")
    print(assessed_students)
