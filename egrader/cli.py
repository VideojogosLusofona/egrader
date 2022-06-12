import argparse
from pathlib import Path
import shutil

OPT_E_SHORT = "-e"
OPT_E_LONG = "--existing"
OPT_E_STOP = "stop"
OPT_E_UPDT = "update"
OPT_E_OVWR = "overwrite"

FILE_REPO_REGISTRY = "repos.yml"


def main():
    """
    This function is called when the script is invoked with the `egrader` command.
    """

    # Create an argument parser
    parser = argparse.ArgumentParser(
        description="Exercise Grader",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        title="commands",
        required=True
    )

    # Create the parser for the "fetch" command
    parser_fetch = subparsers.add_parser(
        "fetch",
        help="Fetch all repositories"
    )
    parser_fetch.add_argument(
        OPT_E_SHORT, OPT_E_LONG,
        choices=[OPT_E_STOP, OPT_E_UPDT, OPT_E_OVWR],
        help=f"Action to take when fetch has already been performed before (default: {OPT_E_STOP})",
        default=OPT_E_STOP
    )

    parser_fetch.add_argument(
        "urls_file",
        metavar="URLS",
        help="Student public Git account URLs file in TSV format",
        nargs=1
    )
    parser_fetch.add_argument(
        "rules_file",
        metavar="RULES",
        help="Assessment rules in YAML format",
        nargs=1
    )
    parser_fetch.add_argument(
        "output_folder",
        metavar="OUTPUT",
        help="Output folder (defaults to RULES minus yaml extension)",
        nargs='?'
    )
    parser_fetch.set_defaults(func=fetch)

    # Create the parser for the "assess" command
    parser_assess = subparsers.add_parser(
        "assess",
        help="Perform assessment"
    )
    parser_assess.add_argument(
        "rules_file",
        type=str,
        metavar="<RULES_FILE>",
        help="Assessment rules in YAML format"
    )
    parser_assess.add_argument(
        "output_folder",
        metavar="OUTPUT",
        help="Output folder (defaults to RULES minus yaml extension)",
        nargs='?'
    )
    parser_assess.set_defaults(func=assess)

    # Parse command line arguments
    args = parser.parse_args()

    # Invoke function to perform selected command
    args.func(args)


def fetch(args):

    # Create file paths
    urls_file = Path(args.urls_file)
    rules_file = Path(args.rules_file)
    if args.output_folder != None:
        output_folder = Path(args.output)
    else:
        output_folder = rules_file.stem

    if output_folder.exists():
        if args.choice == OPT_E_STOP:
            print("Output folder already exists, stopping operation.")
            print(f"To continue anyway see the {OPT_E_SHORT}/{OPT_E_LONG} option.")
            return
        elif args.choice == OPT_E_OVWR:
            print("Output folder already exists, deleting it...")
            shutil.rmdir(output_folder)
            output_folder.mkdir()
    else:
        output_folder.mkdir()

    repo_registry_file = Path(args.output, FILE_REPO_REGISTRY)



def assess(args):
    print("ASSESS!")
    print(args)