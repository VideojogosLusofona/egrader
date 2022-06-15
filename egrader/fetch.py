import shutil
from collections.abc import Sequence
from pathlib import Path
from typing import List

from yarl import URL

from .common import (
    FILE_VALIDATED_GIT_URLS,
    OPT_E_LONG,
    OPT_E_OVWR,
    OPT_E_SHORT,
    OPT_E_STOP,
    Student,
)
from .git import GitError, git, git_at
from .yaml import load_yaml, save_yaml


def fetch(args) -> None:
    """Fetch operation: verify Git URLs, clone or update all repositories."""

    # Create file paths
    urls_fp = Path(args.urls_file[0])
    rules_fp = Path(args.rules_file[0])

    # Check if Git URLs file exists, and if not, quit
    check_required_fp_exists(urls_fp)

    # Check if rules file exists, and if not, quit
    check_required_fp_exists(rules_fp)

    # Determine output folder, either given by user or we extract it from the
    # rules file name
    if args.output_folder is not None:
        output_fp = Path(args.output)
    else:
        output_fp = Path(f"out_{rules_fp.stem}")

    # Create file path for validated URLs yaml file
    validated_urls_fp = output_fp.joinpath(FILE_VALIDATED_GIT_URLS)

    # Check if output folder exists
    if output_fp.exists():

        # If so, action to take depends on the -e command line option
        if getattr(args, OPT_E_LONG) == OPT_E_STOP:

            # Stop processing
            raise FileExistsError(
                "Output folder already exists, stopping operation. Check the "
                f"-{OPT_E_SHORT}/--{OPT_E_LONG} option for alternative behavior."
            )

        elif getattr(args, OPT_E_LONG) == OPT_E_OVWR:

            # Delete folder and its contents and recreate it
            print("Output folder already exists, deleting it...")
            shutil.rmdir(output_fp)
            output_fp.mkdir()
    else:

        # Folder doesn't exist, create it
        output_fp.mkdir()

    # Load rules
    repo_rules = load_yaml(rules_fp)

    # Load student Git URLs
    if validated_urls_fp.exists():

        # If file with validated URLs already exists, load info from there to
        # avoid rechecking the URLs (only with "-e update" option)
        students = load_yaml(validated_urls_fp, safe=False)

    else:

        # Otherwise load info from original file and validate URLs
        students = load_urls(urls_fp)

    # Clone or update student repositories
    fetch_repos(output_fp, students, repo_rules.keys())

    # Save validated URLs and repositories to avoid rechecking them later with
    # the "-e update" option
    save_yaml(validated_urls_fp, students)

    print(students)


def fetch_repos(base_fp: Path, students: Sequence[Student], repos: Sequence[str]):
    """Clone or update student repositories"""

    # Loop through students
    for student in students:
        if student.valid_url:

            # Determine path where to place student repos
            student_path = base_fp.joinpath(student.sid)

            # Loop through mandated repos
            for repo_name in repos:

                # Determine repo URL and local path
                repo_url = URL(student.git_url) / repo_name
                repo_path = student_path.joinpath(repo_name)

                # Does the repository already exist?
                if repo_path.exists():

                    # Path exists, only update repository
                    git_at(repo_path, "pull")

                    # Add repo location to student object
                    student.add_repo(repo_name, str(repo_path))

                else:

                    # Repository doesn't exist, do a full clone
                    try:
                        git("clone", repo_url, repo_path)

                    except GitError:
                        # If a GitException occurs, assume the repo doesn't exist
                        pass

                    else:
                        # Otherwise add repo location to student object
                        student.add_repo(repo_name, str(repo_path))


def check_required_fp_exists(fp_to_check: Path) -> None:
    """Check if file path exists, and if not, raise exception"""
    if not fp_to_check.exists():
        raise FileNotFoundError(f"File '{fp_to_check}' does not exist!")


def load_urls(urls_fp: Path) -> List[Student]:
    """Load student Git URLs"""

    # The student list, initially empty
    students: List[Student] = []

    # Open Git URLs file
    with open(urls_fp) as urls_file:

        # Cycle through each line of the file
        for lno, line in enumerate(urls_file, 1):

            # Remove leading and trailing whitespace
            line = line.strip()

            # Ignore line if it's empty or starts with # (comment)
            if len(line) == 0 or line[0] == "#":
                continue

            # Split line and check that it's composed of two chunks
            std_url = line.split()
            if len(std_url) != 2:
                raise SyntaxError(
                    f"Syntax error in line {lno} of {urls_fp}: " f"'{line}'"
                )

            # Create a student instance with it's ID and URL, taken from the line
            student = Student(std_url[0], std_url[1])

            # Append new student to the student list
            students.append(student)

    # Return students
    return students
