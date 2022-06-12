import argparse
import sys
from pathlib import Path

import pygit2 as git
import yaml
from yarl import URL

from .Student import Student

ERR_GIT_URLS_FILE_NOT_EXIST = 1
ERR_RULES_FILE_NOT_EXIST = 2
ERR_GIT_URLS_FILE_INVALID = 3

RESULTS_FILE = "results.yml"


def main():
    """
    This function is called when the script is invoked with the `egrader` command.
    """

    # Create an argument parser
    parser = argparse.ArgumentParser(
        description="Exercise Grader.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Specify arguments to parse
    parser.add_argument(
        "-g",
        "--git-urls",
        type=str,
        metavar="<GIT URLS FILE>",
        help="Student public Git account URLs file in TSV format",
        required=True,
    )
    parser.add_argument(
        "-r",
        "--rules",
        type=str,
        metavar="<RULES FILE>",
        help="Assessment rules in YAML format",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="<OUTPUT FOLDER>",
        help="Output folder",
        required=True,
    )

    on_existing_action = parser.add_mutually_exclusive_group()
    on_existing_action.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite all repositories and results even if they already exist locally",
        default=False,
    )
    on_existing_action.add_argument(
        "--update",
        action="store_true",
        help="If repositories already exist locally, check for remote updates",
        default=False,
    )

    # Parse and validate command line arguments
    args = parser.parse_args()

    # Create file paths
    git_urls_file = Path(args.git_urls)
    rules_file = Path(args.rules)
    output_folder = Path(args.output)
    results_file = Path(args.output, RESULTS_FILE)

    # Check if Git URLs file exists, and if not, quit
    if not git_urls_file.exists():
        print(f"File '{git_urls_file}' does not exist!", file=sys.stderr)
        exit(ERR_GIT_URLS_FILE_NOT_EXIST)

    # Check if rules file exists, and if not, quit
    if not rules_file.exists():
        print(f"File '{rules_file}' does not exist!", file=sys.stderr)
        exit(ERR_RULES_FILE_NOT_EXIST)

    # Check if output folder exists, and if not, create it
    if not output_folder.exists():
        Path.mkdir(output_folder)

    # Check if results file exists, and if so load results from it
    if results_file.exists():
        # Load results from results file
        results = yaml.safe_load(results_file.read_text())

    else:
        # Generate new results

        # Open rules file
        with open(rules_file, 'r') as rf:
            repo_rules = yaml.safe_load(rf)

        # Create student list with respective URLs
        # students = [
        #     Student("1234354", "http://www.myurl.com/"),
        #     Student("1423567", "http://www.ouurl.com/")
        # ]
        students = []
        with open(git_urls_file) as gufile:
            for line in gufile:
                std_url = line.split(maxsplit=2)
                if len(std_url) != 2:
                    print(
                        f"File '{git_urls_file}' is not properly formatted!",
                        file=sys.stderr,
                    )
                    exit(ERR_GIT_URLS_FILE_INVALID)
                student = Student(std_url[0], std_url[1])
                students.append(student)

                # If the student URL is valid, check for repos
                if student.valid_url:

                    # Create a folder for the student if it doesn't already exist
                    student_folder = Path(args.output, student.sid)

                    if not student_folder.exists():
                        Path.mkdir(student_folder)

                    # Cycle through repository rules
                    for repo_rule in repo_rules:

                        # Form repo URL (student URL + repo name)
                        repo_url = URL(student.git_url) / repo_rule.name

                        # Form path where to clone repo
                        repo_path = Path(student_folder, repo_rule.name)

                        # Clone repository and apply checks
                        try:
                            repo = git.clone_repository(repo_url, repo_url)
                        except:
                            # Student doesn't have the current repo, try the
                            # next one
                            continue




        # Create and save results
        print(yaml.dump(students), file=open(results_file, "w"))

    # Cycle through students
    for s in students:
        # Show validity of students' URLs
        print(s.sid, s.git_url, s.valid_url)

        # Does the student URL contain
