from importlib.metadata import entry_points
from pathlib import Path

from .common import check_required_fp_exists, get_output_fp, get_valid_student_urls_fp
from .yaml import load_yaml


def assess(args) -> None:
    """Perform student assessment"""

    # Determine rules file path
    rules_fp: Path = Path(args.rules_file[0])

    # Check if rules file exists, and if not, quit
    check_required_fp_exists(rules_fp)

    # Determine output folder, either given by user or we extract it from the
    # rules file name
    output_fp: Path = get_output_fp(args.output_folder, rules_fp)

    # Check if output folder exists, and if not, quit
    check_required_fp_exists(output_fp)

    # Determine file path for valid student URLs yaml file
    student_urls_fp: Path = get_valid_student_urls_fp(output_fp)

    # Check if valid student URLs yaml file exists, and if not, quit
    check_required_fp_exists(student_urls_fp)

    # Load rules
    rules = load_yaml(rules_fp)

    # Load student list and their URLs
    students = load_yaml(student_urls_fp, safe=False)

    # Load assessment plugins
    assess_plugins = entry_points(group="egrader.assess")

    print(rules)
    print()
    print(students)
    print()
    print(assess_plugins)