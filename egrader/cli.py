import argparse
import sys
from pathlib import Path

from egrader.Student import Student

ERR_GIT_URLS_FILE_NOT_EXIST = 1
ERR_RULES_FILE_NOT_EXIST = 2
ERR_GIT_URLS_FILE_INVALID = 3


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

    # Parse and validate command line arguments
    args = parser.parse_args()

    # Create file paths
    git_urls_file = Path(args.git_urls)
    rules_file = Path(args.rules)
    output_folder = Path(args.output)

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

    # Create student list with respective URLs
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
            students.append(Student(std_url[0], std_url[1]))

    # Show validity of students' URLs
    for s in students:
        print(s.sid, s.git_url, s.valid_url)
