import argparse
from collections.abc import Sequence
from pathlib import Path
import shutil
import sys
from typing import Any

import yaml

from .Student import Student

OPT_E_SHORT = "e"
OPT_E_LONG = "existing"
OPT_E_STOP = "stop"
OPT_E_UPDT = "update"
OPT_E_OVWR = "overwrite"

FILE_VALIDATED_GIT_URLS = "validated_git_urls.yml"


def main():
    """
    This function is called when the script is invoked with the `egrader` command.
    """

    # Create an argument parser
    parser = argparse.ArgumentParser(
        description="Exercise Grader",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Debug flag for showing full stack traces when errors occur
    parser.add_argument(
        "--debug",
        action="store_true",
        help="show complete exception traceback when an error occurs"
    )

    # Allow for subcommands
    subparsers = parser.add_subparsers(
        title="commands",
        required=True
    )

    # Create the parser for the "fetch" command
    parser_fetch = subparsers.add_parser(
        "fetch",
        help="fetch all repositories"
    )
    parser_fetch.add_argument(
        f"-{OPT_E_SHORT}", f"--{OPT_E_LONG}",
        choices=[OPT_E_STOP, OPT_E_UPDT, OPT_E_OVWR],
        help=f"action to take when fetch has already been performed before (default: {OPT_E_STOP})",
        default=OPT_E_STOP
    )

    parser_fetch.add_argument(
        "urls_file",
        metavar="URLS",
        help="student public Git account URLs file in TSV format",
        nargs=1
    )
    parser_fetch.add_argument(
        "rules_file",
        metavar="RULES",
        help="assessment rules in YAML format",
        nargs=1
    )
    parser_fetch.add_argument(
        "output_folder",
        metavar="OUTPUT",
        help="output folder (defaults to RULES minus yaml extension)",
        nargs='?'
    )
    parser_fetch.set_defaults(func=fetch)

    # Create the parser for the "assess" command
    parser_assess = subparsers.add_parser(
        "assess",
        help="perform assessment"
    )
    parser_assess.add_argument(
        "rules_file",
        type=str,
        metavar="<RULES_FILE>",
        help="assessment rules in YAML format"
    )
    parser_assess.add_argument(
        "output_folder",
        metavar="OUTPUT",
        help="output folder (defaults to RULES minus yaml extension)",
        nargs='?'
    )
    parser_assess.set_defaults(func=assess)

    # Parse command line arguments
    args = parser.parse_args()

    # Invoke function to perform selected command
    try:
        args.func(args)
    except (FileNotFoundError, FileExistsError, SyntaxError) as e:
        print(e.args[0], file=sys.stderr)
        if (args.debug):
            print("-------- Exception details --------", file=sys.stderr)
            raise e
        return 1
    else:
        print("Program terminated successfully.")
        return 0


def fetch(args) -> None:
    """Fetch operation: clone or update all repositories."""

    # Create file paths
    urls_fp = Path(args.urls_file[0])
    rules_fp = Path(args.rules_file[0])

    # Check if Git URLs file exists, and if not, quit
    check_required_fp_exists(urls_fp)

    # Check if rules file exists, and if not, quit
    check_required_fp_exists(rules_fp)

    # Determine output folder, either given by user or we extract it from the
    # rules file name
    if args.output_folder != None:
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
            raise FileExistsError("Output folder already exists, stopping operation. "\
                f"Check the -{OPT_E_SHORT}/--{OPT_E_LONG} option for alternative behavior.")

        elif  getattr(args, OPT_E_LONG) == OPT_E_OVWR:

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
        students = load_yaml(validated_urls_fp)

    else:

        # Otherwise load info from original file and validate URLs
        students = load_urls(urls_fp)

        # Save validated URLs to avoid rechecking them later with the "-e update"
        # option
        save_yaml(validated_urls_fp, students)

    print(students)


def assess(args) -> None:
    print("ASSESS!")
    print(args)


def load_yaml(yaml_fp: Path) -> Any:
    """Load a yaml file"""
    try:
        with open(yaml_fp, "r") as yaml_file:
            yaml_obj = yaml.safe_load(yaml_file)
    except yaml.scanner.ScannerError as se:
        raise SyntaxError(f"Syntax error{se.problem_mark} {se.context}: {se.problem}") from se

    return yaml_obj


def save_yaml(yaml_fp: Path, data: Any) -> None:
    """Save a yaml file"""

    yaml_text = yaml.dump(data)
    print(yaml_text, file=open(yaml_fp, "w"))


def check_required_fp_exists(fp_to_check: Path) -> None:
    """ Check if file path exists, and if not, raise exception"""
    if not fp_to_check.exists():
        raise FileNotFoundError(f"File '{fp_to_check}' does not exist!")


def load_urls(urls_fp: Path) -> Sequence[Student]:
    """Load student Git URLs"""

    # The student list, initially empty
    students: list[Student] = []

    # Open Git URLs file
    with open(urls_fp) as urls_file:

        # Cycle through each line of the file
        for lno, line in enumerate(urls_file, 1):

            # Remove leading and trailing whitespace
            line = line.strip()

            # Ignore line if it's empty or starts with # (comment)
            if len(line) == 0 or line[0] == '#':
                continue

            # Split line and check that it's composed of two chunks
            std_url = line.split()
            if len(std_url) != 2:
                raise SyntaxError(f"Syntax error in line {lno} of {urls_fp}: "\
                    f"'{line}'")

            # Create a student instance with it's ID and URL, taken from the line
            student = Student(std_url[0], std_url[1])

            # Append new student to the student list
            students.append(student)

    # Return students
    return students

