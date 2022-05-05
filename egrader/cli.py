import argparse
import sys
from pathlib import Path

import yaml

from .Results import Results
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
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force redownload of all repositories even if they already exist locally",
        default=False,
    )
    parser.add_argument(
        "-u",
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
                student.validate()
                students.append(student)

        # Create and save results
        results = Results(students)
        print(yaml.dump(results), file=open(results_file, "w"))

    # Show validity of students' URLs
    for s in results.students:
        print(s.sid, s.git_url, s.valid_url)

    # Open rules file
    with open(rules_file, 'r') as rf:
        rules = yaml.safe_load(rf)