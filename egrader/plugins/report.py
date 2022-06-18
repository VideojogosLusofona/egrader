from datetime import datetime
from typing import Sequence

from ..common import AssessedStudent, check_empty_args


def report_markdown_basic(
    assessed_students: Sequence[AssessedStudent], args: Sequence[str]
):
    """Generate a basic Markdown assessment report."""

    # args should be empty
    check_empty_args(args)

    print("# Assessment report")
    print()
    print(datetime.now().ctime())
    print()

    for student in assessed_students:
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


def report_stdout_basic(
    assessed_students: Sequence[AssessedStudent], args: Sequence[str]
):
    """Generate a basic assessment report directly to the standard output."""

    # args should be empty
    check_empty_args(args)

    for student in assessed_students:
        print(f"- Student: {student.sid}")
        print(f"\tGrade: {student.grade}")
