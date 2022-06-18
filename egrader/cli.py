import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentError, ArgumentParser

from sh import ErrorReturnCode

from .assess import assess
from .common import OPT_E_LONG, OPT_E_OVWR, OPT_E_SHORT, OPT_E_STOP, OPT_E_UPDT
from .fetch import fetch
from .plugins.report import report_stdout_basic
from .plugins_helper import LoadPluginError, list_plugins
from .report import report


def main():
    """
    This function is called when the script is invoked with the `egrader` command.
    """

    # Create an argument parser
    parser = ArgumentParser(
        description="Exercise Grader",
        formatter_class=ArgumentDefaultsHelpFormatter,
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
        "assess_folder",
        metavar="ASSESS_FOLDER",
        help="Folder where assessment data will be placed (defaults to RULES "
        "minus yaml extension)",
        nargs="?",
    )
    parser_fetch.set_defaults(func=fetch)

    # Create the parser for the "assess" command
    parser_assess = subparsers.add_parser("assess", help="perform assessment")
    parser_assess.add_argument(
        "rules_file", metavar="RULES", help="assessment rules in YAML format", nargs=1
    )
    parser_assess.add_argument(
        "assess_folder",
        metavar="ASSESS_FOLDER",
        help="Folder where assessment data is located (defaults to RULES "
        "minus yaml extension)",
        nargs="?",
    )
    parser_assess.set_defaults(func=assess)

    # Create the parser for the "report" command
    parser_report = subparsers.add_parser(
        "report", help="generate an assessment report"
    )
    parser_report.add_argument(
        "assess_folder",
        metavar="ASSESS_FOLDER",
        help="Folder where assessment data is located",
        nargs=1,
    )
    default_report = report_stdout_basic.__name__[len(report.__name__) + 1 :]
    parser_report.add_argument(
        "report_type",
        metavar="REPORT_TYPE [REPORT_ARGS ...]",
        help=f"Type of report and report arguments (defaults to {default_report})",
        default=default_report,
        nargs="?",
    )
    parser_report.set_defaults(func=report)

    # Create the parser for the "plugins" command
    parser_plugins = subparsers.add_parser("plugins", help="list available plugins")
    parser_plugins.set_defaults(func=list_plugins)

    # Parse command line arguments
    args = parser.parse_known_args()

    # Invoke function to perform selected command
    try:
        args[0].func(args[0], args[1])
    except (
        FileNotFoundError,
        FileExistsError,
        SyntaxError,
        ErrorReturnCode,
        LoadPluginError,
    ) as e:
        print(e.args[0], file=sys.stderr)
        if args[0].debug:
            print("-------- Exception details --------", file=sys.stderr)
            raise e
        return 1
    except ArgumentError as e:
        print(e.message, file=sys.stderr)
        if args[0].debug:
            print("-------- Exception details --------", file=sys.stderr)
            raise e
        return 1
    else:
        return 0
