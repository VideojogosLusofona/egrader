from argparse import Namespace
from pathlib import Path
from typing import Sequence, cast

from .paths import check_required_fp_exists, get_assessed_students_fp
from .plugin import PLUGINS_REPORT, load_plugin_function
from .types import AssessedStudent
from .yaml import load_yaml


def report(assess_fp: Path, args: Namespace, extra_args: Sequence[str]) -> None:
    """Generate an assessment report."""

    # Determine report file path
    assess_file_fp: Path = get_assessed_students_fp(assess_fp)

    # Check if assessment file exists, and if not, quit
    check_required_fp_exists(assess_file_fp)

    # Load report file
    assessed_students: Sequence[AssessedStudent] = cast(
        Sequence[AssessedStudent], load_yaml(assess_file_fp, False)
    )

    # Load plugin function to perform reporting
    report_fun = load_plugin_function(PLUGINS_REPORT, args.report_type)

    # Invoke reporting function with the specified arguments, if any
    report_fun(assess_fp, assessed_students, extra_args)
