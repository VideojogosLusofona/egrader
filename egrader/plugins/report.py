from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Final, Sequence

from ..cli_lib import CLIArgError, check_empty_args
from ..paths import get_student_repo_fp
from ..types import AssessedStudent

_FILE_STUDENT_REPORT_MD_: Final[str] = "report.md"


def report_markdown_basic(
    assess_fp: Path, assessed_students: Sequence[AssessedStudent], args: Sequence[str]
) -> str:
    """Generate a basic Markdown assessment report."""

    # Print the report's header
    def print_header() -> None:
        print("# Assessment report")
        print()
        print(datetime.now().ctime())
        print()

    # Print the detailed student assessment
    def print_student(student: AssessedStudent) -> None:
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

    # Report output to main program
    rep_output: str

    # Save report to separate files?
    to_files: bool = False

    # Check parameters (only '-f' is acceptable, to enable saving report to files)
    if len(args) == 1 and args[0] == "-f":
        to_files = True
    elif len(args) >= 1:
        raise CLIArgError(f"Invalid arguments: {', '.join(args)}")

    if to_files:
        with StringIO() as out_string:
            print(f"- Absolute assessment path: {assess_fp.absolute()}.")

            # Save individual reports to a file for each student
            for student in assessed_students:
                report_fp = get_student_repo_fp(
                    assess_fp, student.sid, _FILE_STUDENT_REPORT_MD_
                )
                with open(report_fp, "w") as md_file, redirect_stdout(md_file):
                    print_header()
                    print_student(student)

                print(
                    f"- Assessment report for student {student.sid} saved at "
                    f"{report_fp}.",
                    file=out_string,
                )

            rep_output = out_string.getvalue()

    else:
        # Print report to report output string
        with StringIO() as md_string, redirect_stdout(md_string):
            print_header()
            for student in assessed_students:
                print_student(student)
            rep_output = md_string.getvalue()

    return rep_output


def report_stdout_basic(
    assess_fp: Path, assessed_students: Sequence[AssessedStudent], args: Sequence[str]
) -> str:
    """Generate a basic assessment report directly to the standard output."""

    # args should be empty
    check_empty_args(args)

    with StringIO() as out_text, redirect_stdout(out_text):
        for student in assessed_students:
            print(f"- Student: {student.sid}")
            print(f"\tGrade: {student.grade}")
        return out_text.getvalue()
