import sys
from argparse import ArgumentError
from contextlib import redirect_stdout
from datetime import datetime
from io import TextIOWrapper
from pathlib import Path
from typing import Sequence, cast

from ..common import AssessedStudent, check_empty_args


def report_markdown_basic(
    assess_fp: Path, assessed_students: Sequence[AssessedStudent], args: Sequence[str]
):
    """Generate a basic Markdown assessment report."""

    # Save report to separate files?
    to_files: bool = False

    # Check parameters (only '-f' is acceptable, to enable saving report to files)
    if len(args) == 1 and args[0] == "-f":
        to_files = True
    elif len(args) >= 1:
        raise ArgumentError(None, f"Invalid arguments: {', '.join(args)}")

    def print_header():
        print("# Assessment report")
        print()
        print(datetime.now().ctime())
        print()

    if not to_files:
        print_header()

    for student in assessed_students:

        f: TextIOWrapper

        if to_files:
            f = open(f"{student.sid}.md", "w")
        else:
            f = cast(TextIOWrapper, sys.stdout)

        with redirect_stdout(f):

            if to_files:
                print_header()

            print(f"## Student {student.sid}")
            print()
            print(f"- Grade: {student.grade}")
            print()
            print("### Repositories")
            print()
            for repo in student.assessed_repos:
                print(f"#### {repo.name}")
                print()
                print(f"- Weight in grade: {repo.weight}")
                print(f"- Grade (unweighted): {repo.grade_raw}")
                print(f"- Final grade: {repo.grade_final}")
                print()
                print("##### Assessments")
                print()
                if repo.is_empty():
                    print("Repository not available and/or no assessments performed.")
                for assess in repo.assessments + repo.inter_assessments:
                    print(f"- `{assess.name}`")
                    print(f"  - Description: {assess.description}")
                    print(f"  - Parameters: `{assess.parameters}`")
                    print(f"  - Weight in grade: {assess.weight}")
                    print(f"  - Grade (unweighted): {assess.grade_raw}")
                    print(f"  - Final grade: {assess.grade_final}")
                    print()

        if to_files:
            f.close()


def report_stdout_basic(
    assess_fp: Path, assessed_students: Sequence[AssessedStudent], args: Sequence[str]
):
    """Generate a basic assessment report directly to the standard output."""

    # args should be empty
    check_empty_args(args)

    for student in assessed_students:
        print(f"- Student: {student.sid}")
        print(f"\tGrade: {student.grade}")
