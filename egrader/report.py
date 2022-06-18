from pathlib import Path

from .common import FILE_ASSESSED_STUDENTS, check_required_fp_exists, get_assess_fp
from .plugins_helper import PLUGINS_REPORT, load_plugin_function
from .yaml import load_yaml


def report(args) -> None:
    """Generate an assessment report."""

    # Determine assessment folder, either given by user or we extract it from
    # the rules file name
    assess_folder_fp: Path = get_assess_fp(args.assess_folder[0], None)

    # Determine report file path
    assess_file_fp: Path = assess_folder_fp.joinpath(FILE_ASSESSED_STUDENTS)

    # Check if assessment file exists, and if not, quit
    check_required_fp_exists(assess_file_fp)

    # Load report file
    assessed_students = load_yaml(assess_file_fp, False)

    # Load plugin function to perform reporting
    report_fun = load_plugin_function(PLUGINS_REPORT, args.report_type)

    # Invoke reporting function with the specified arguments, if any
    report_fun(assessed_students, *args.report_args)
