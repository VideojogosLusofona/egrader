import argparse
from pathlib import Path
import shutil
import sys
import yaml

OPT_E_SHORT = "e"
OPT_E_LONG = "existing"
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
        f"-{OPT_E_SHORT}", f"--{OPT_E_LONG}",
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
    try:
        args.func(args)
    except (FileNotFoundError, FileExistsError) as e:
        print(e.args[0], file=sys.stderr)
        # print(getattr(e, "message", repr(e)), file=sys.stderr)
        return 1
    except Exception as e:
        raise e
    else:
        print("Program terminated successfully.")
        return 0


def fetch(args):
    """Fetch operation: clone or update all repositories."""

    # Create file paths
    urls_file = Path(args.urls_file[0])
    rules_file = Path(args.rules_file[0])

    # Check if Git URLs file exists, and if not, quit
    check_required_file_exists(urls_file)

    # Check if rules file exists, and if not, quit
    check_required_file_exists(rules_file)

    # Determine output folder, either given by user or we extract it from the
    # rules file name
    if args.output_folder != None:
        output_folder = Path(args.output)
    else:
        output_folder = Path(f"out_{rules_file.stem}")

    # Check if output folder exists
    if output_folder.exists():
        # If so, action to take depends on the -e command line option
        if getattr(args, OPT_E_LONG) == OPT_E_STOP:
            # Stop processing
            raise FileExistsError("Output folder already exists, stopping operation. "\
                f"Check the -{OPT_E_SHORT}/--{OPT_E_LONG} option for alternative behavior.")
        elif  getattr(args, OPT_E_LONG) == OPT_E_OVWR:
            # Delete folder and its contents and recreate it
            print("Output folder already exists, deleting it...")
            shutil.rmdir(output_folder)
            output_folder.mkdir()
    else:
        # Folder doesn't exist, create it
        output_folder.mkdir()

    # Load rules
    with open(rules_file, 'r') as rf:
        repo_rules = yaml.safe_load(rf)


    #repo_registry_file = Path(args.output, FILE_REPO_REGISTRY)

def assess(args):
    print("ASSESS!")
    print(args)


def check_required_file_exists(file_to_check: Path):
    """ Check if file exists, and if not, quit"""
    if not file_to_check.exists():
        raise FileNotFoundError(f"File '{file_to_check}' does not exist!")

