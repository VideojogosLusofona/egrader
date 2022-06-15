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

    # Create a set of all required assessments
    required_assessments = set()
    for rule in rules:
        for assessment in rule["assessments"]:
            required_assessments.add(assessment["name"])

    # Load required assessment plugins as specified by the rules
    assess_functions = {}
    for ap in assess_plugins:
        if ap.name in required_assessments:
            assess_functions[ap.name] = ap.load()
        else:
            # TODO Raise error
            pass

    # Apply rules and assessments to each student
    for student in students:
        for rule in rules:
            if rule["repo"] in student.repos:
                for assessment in rule["assessments"]:
                    assess_fun = assess_functions[assessment["name"]]
                    repo_local_path = student.repos[rule["repo"]]
                    assess_params = assessment["params"]
                    assess_fun(repo_local_path, **assess_params)
