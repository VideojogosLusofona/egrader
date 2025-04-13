"""The egrader command-line interface."""

import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Final

from sh import ErrorReturnCode

from .assess import assess
from .cli_lib import (
    OPT_E_LONG,
    OPT_E_OVWR,
    OPT_E_SHORT,
    OPT_E_STOP,
    OPT_E_UPDT,
    CLIArgError,
)
from .fetch import fetch
from .plugin import PluginLoadError, list_plugins
from .plugins.report import report_basic
from .report import report

_ASSESS_FOLDER_ATTR: Final[str] = "assess_folder"
_RULES_FILE_ATTR: Final[str] = "rules_file"
_FOLDER_ASSESS_DEFAULT_PREFIX: Final[str] = "out_"


def main():
    """Function invoked with the `egrader` command."""
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
        "-w",
        "--wait",
        help="time in seconds to wait between clones/fetches (default: 0)",
        metavar="SECS",
        type=float,
        default=0,
    )

    parser_fetch.add_argument(
        "urls_file",
        metavar="URLS",
        help="student public Git account URLs file in TSV format",
    )
    parser_fetch.add_argument(
        _RULES_FILE_ATTR,
        metavar=_RULES_FILE_ATTR.upper(),
        help="assessment rules in YAML format",
    )
    parser_fetch.add_argument(
        _ASSESS_FOLDER_ATTR,
        metavar=_ASSESS_FOLDER_ATTR.upper(),
        help="Folder where assessment data will be placed (defaults to RULES "
        "minus yaml extension)",
        nargs="?",
    )
    parser_fetch.set_defaults(func=fetch)

    # Create the parser for the "assess" command
    parser_assess = subparsers.add_parser("assess", help="perform assessment")
    parser_assess.add_argument(
        _RULES_FILE_ATTR,
        metavar=_RULES_FILE_ATTR.upper(),
        help="assessment rules in YAML format",
    )
    parser_assess.add_argument(
        _ASSESS_FOLDER_ATTR,
        metavar=_ASSESS_FOLDER_ATTR.upper(),
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
        _ASSESS_FOLDER_ATTR,
        metavar=_ASSESS_FOLDER_ATTR.upper(),
        help="Folder where assessment data is located",
    )
    default_report = report_basic.__name__[len(report.__name__) + 1 :]
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

    # Determine assessment folder
    assess_folder = getattr(args[0], _ASSESS_FOLDER_ATTR, None)
    rules_file = getattr(args[0], _RULES_FILE_ATTR, None)

    if assess_folder is None and rules_file is None and args[0].func != list_plugins:
        # This should not be possible
        raise AssertionError(
            f"{_ASSESS_FOLDER_ATTR.upper()} and {_RULES_FILE_ATTR.upper()} "
            "parameters cannot be None simultaneously!"
        )

    # Assessment folder path can be given by user or obtained from the rules file name
    if assess_folder is not None:
        assess_fp = Path(assess_folder)
    elif rules_file is not None:
        assess_fp = Path(f"{_FOLDER_ASSESS_DEFAULT_PREFIX}{Path(rules_file).stem}")
    else:
        assess_fp = None

    # Invoke function to perform selected command
    try:
        with StringIO() as out_stream, redirect_stdout(out_stream):
            args[0].func(assess_fp, args[0], args[1])
            out_string = out_stream.getvalue()
    except (
        ErrorReturnCode,
        FileNotFoundError,
        FileExistsError,
        CLIArgError,
        PluginLoadError,
        SyntaxError,
    ) as e:
        print(e.args[0], file=sys.stderr)
        if args[0].debug:
            print("-------- Exception details --------", file=sys.stderr)
            raise e
        return 1
    else:
        print(out_string, end="")
        return 0
