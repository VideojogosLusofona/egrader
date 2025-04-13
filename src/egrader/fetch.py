"""Functions for fetching code from student repositories."""

import shutil
from argparse import Namespace
from pathlib import Path
from time import sleep
from typing import List, Sequence

from .cli_lib import OPT_E_LONG, OPT_E_OVWR, OPT_E_SHORT, OPT_E_STOP, check_empty_args
from .git import GitError, git, git_at
from .paths import (
    check_required_fp_exists,
    get_student_repo_fp,
    get_student_repos_fp,
    get_valid_students_git_fp,
)
from .types import StudentGit
from .yaml import load_yaml, save_yaml


def fetch(assess_fp: Path, args: Namespace, extra_args: Sequence[str]) -> None:
    """Fetch operation: verify Git URLs, clone or update all repositories."""
    print(f"- Absolute assessment path: {assess_fp.absolute()}.")

    # extra_args should be empty
    check_empty_args(extra_args)

    # Determine file paths for Git URLs and rules files
    urls_fp: Path = Path(args.urls_file)
    rules_fp: Path = Path(args.rules_file)

    # Time to wait between fetches
    wait_time: float = args.wait

    # Check if Git URLs file exists, and if not, quit
    check_required_fp_exists(urls_fp)

    # Check if rules file exists, and if not, quit
    check_required_fp_exists(rules_fp)

    # Determine file path for validated URLs yaml file
    students_git_fp: Path = get_valid_students_git_fp(assess_fp)

    # Check if the assessment output folder exists
    if assess_fp.exists():
        # If so, action to take depends on the -e command line option
        if getattr(args, OPT_E_LONG) == OPT_E_STOP:
            # Stop processing
            raise FileExistsError(
                "Assessment folder already exists, stopping operation. Check the "
                f"-{OPT_E_SHORT}/--{OPT_E_LONG} option for alternative behavior."
            )

        elif getattr(args, OPT_E_LONG) == OPT_E_OVWR:
            # Delete folder and its contents and recreate it
            print(f"- Assessment folder already exists at {assess_fp}, deleting it.")
            shutil.rmtree(assess_fp)
            assess_fp.mkdir()
    else:
        # Folder doesn't exist, create it
        assess_fp.mkdir()

    # Load rules
    repo_rules = load_yaml(rules_fp)

    # Declare list of student valid Git URLs
    students_git: List[StudentGit]

    # Load student Git URLs
    if students_git_fp.exists():
        # If file with validated URLs already exists, load info from there to
        # avoid rechecking the URLs (only with "-e update" option)
        students_git = load_yaml(students_git_fp, safe=False)

    else:
        # Otherwise load info from original file and validate URLs
        students_git = load_urls(urls_fp)

    # Clone or update student repositories
    n_valid_urls = fetch_repos(
        assess_fp, students_git, [rule["repo"] for rule in repo_rules], wait_time
    )

    # Determine number of repositories
    n_repos = sum([s.repo_count for s in students_git])

    # Save validated URLs and repositories to avoid rechecking them later with
    # the "-e update" option
    save_yaml(students_git_fp, students_git)

    # Provide feedback to the user
    print(
        f"- Fetched {n_repos} repositories from {len(students_git)} students, "
        f"{n_valid_urls} of which with valid URLs."
    )
    print(f"- Repositories saved at {get_student_repos_fp(assess_fp)}.")
    print(f"- URL and repository validation report available at {students_git_fp}.")


def fetch_repos(
    assess_fp: Path,
    students_git: Sequence[StudentGit],
    repos: Sequence[str],
    wait_time: float,
) -> int:
    """Clone or update student repositories."""
    # Number of valid Git URLs
    n_valid_urls = 0

    # Already fetched/cloned anything?
    any_fetch = False

    # Loop through students
    for student_git in students_git:
        if student_git.valid_url:
            n_valid_urls += 1

            # Loop through mandated repos
            for repo_name in repos:
                # If a fetch/clone was already done, then wait the number of seconds
                # specified by the user
                if any_fetch:
                    sleep(wait_time)

                # Determine repo URL and local path
                repo_url: str = student_git.repo_url(repo_name)
                repo_fp: Path = get_student_repo_fp(
                    assess_fp, student_git.sid, repo_name
                )

                # Does the repository already exist?
                if repo_fp.exists():
                    # Path exists, only update repository
                    git_at(repo_fp, "pull")

                    # Add repo location to student object
                    student_git.add_repo(repo_name, str(repo_fp))

                else:
                    # Repository doesn't exist, do a full clone
                    try:
                        git("clone", repo_url, repo_fp)

                    except GitError:
                        # If a GitException occurs, assume the repo doesn't exist
                        pass

                    else:
                        # Otherwise add repo location to student object
                        student_git.add_repo(repo_name, str(repo_fp))

                # Indicate that at least one fetch/clone has been made
                any_fetch = True

    return n_valid_urls


def load_urls(urls_fp: Path) -> List[StudentGit]:
    """Load student Git URLs."""
    # The student list, initially empty
    students_git: List[StudentGit] = []

    # Open Git URLs file
    with open(urls_fp) as urls_file:
        # Cycle through each line of the file
        for lno, line in enumerate(urls_file, 1):
            # Remove leading and trailing whitespace
            line = line.strip()

            # Ignore line if it's empty or starts with # (comment)
            if len(line) == 0 or line[0] == "#":
                continue

            # Split line and check that it's composed of three chunks
            std_url = line.split()
            if len(std_url) != 3:
                raise SyntaxError(
                    f"Syntax error in line {lno} of {urls_fp}: " f"{line!r}"
                )

            # Create a student instance with it's ID and URL, taken from the line
            student_git = StudentGit(std_url[0], std_url[1], std_url[2])

            # Append new student to the student list
            students_git.append(student_git)

    # Return students
    return students_git
