import argparse
import sys

import sh

from .assess import assess
from .common import OPT_E_LONG, OPT_E_OVWR, OPT_E_SHORT, OPT_E_STOP, OPT_E_UPDT
from .fetch import fetch


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
        help="show complete exception traceback when an error occurs",
    )

    # Allow for subcommands
    subparsers = parser.add_subparsers(title="commands", required=True)

    # Create the parser for the "fetch" command
    parser_fetch = subparsers.add_parser("fetch", help="fetch all repositories")
    parser_fetch.add_argument(
        f"-{OPT_E_SHORT}",
        f"--{OPT_E_LONG}",
        choices=[OPT_E_STOP, OPT_E_UPDT, OPT_E_OVWR],
        help="action to take when fetch has already been performed before "
        f"(default: {OPT_E_STOP})",
        default=OPT_E_STOP,
    )

    parser_fetch.add_argument(
        "urls_file",
        metavar="URLS",
        help="student public Git account URLs file in TSV format",
        nargs=1,
    )
    parser_fetch.add_argument(
        "rules_file", metavar="RULES", help="assessment rules in YAML format", nargs=1
    )
    parser_fetch.add_argument(
        "output_folder",
        metavar="OUTPUT",
        help="output folder (defaults to RULES minus yaml extension)",
        nargs="?",
    )
    parser_fetch.set_defaults(func=fetch)

    # Create the parser for the "assess" command
    parser_assess = subparsers.add_parser("assess", help="perform assessment")
    parser_assess.add_argument(
        "rules_file",
        type=str,
        metavar="RULES",
        help="assessment rules in YAML format",
    )
    parser_assess.add_argument(
        "output_folder",
        metavar="OUTPUT",
        help="output folder (defaults to RULES minus yaml extension)",
        nargs="?",
    )
    parser_assess.set_defaults(func=assess)

    # Parse command line arguments
    args = parser.parse_args()

    # Invoke function to perform selected command
    try:
        args.func(args)
    except (FileNotFoundError, FileExistsError, SyntaxError, sh.ErrorReturnCode) as e:
        print(e.args[0], file=sys.stderr)
        if args.debug:
            print("-------- Exception details --------", file=sys.stderr)
            raise e
        return 1
    else:
        print("Program terminated successfully.")
        return 0
