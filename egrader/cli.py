import argparse


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
        "-e", "--existing",
        choices=["stop", "update", "overwrite"],
        help="Action to take when fetch has already been performed before (default: stop)",
        default="stop"
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
    print("FETCH!")
    print(args)


def assess(args):
    print("ASSESS!")
    print(args)