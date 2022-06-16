from importlib.metadata import entry_points
from pathlib import Path

from .common import check_required_fp_exists, get_output_fp, get_valid_students_git_fp
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

    # Determine file path for valid students Git URL and repos yaml file
    students_git_fp: Path = get_valid_students_git_fp(output_fp)

    # Check if valid students Git URL yaml file exists, and if not, quit
    check_required_fp_exists(students_git_fp)

    # Load rules
    rules = load_yaml(rules_fp)

    # Load student list and their URLs
    students_git = load_yaml(students_git_fp, safe=False)

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
    for student_git in students_git:

        # Current student's grade starts at zero
        student_grade = 0

        # Loop through rules
        for rule in rules:

            # Get the weight of the current rule
            rule_weight = rule["weight"]

            # Current rule's grade starts at zero
            rule_grade = 0

            # If student has the repository specified in the current rule, apply
            # the specified assessments
            if rule["repo"] in student_git.repos:

                # Loop through the assessments to be made for the current rule's
                # repository
                for assessment in rule["assessments"]:

                    # Get the weight of the current assessment within the current
                    # rule
                    assessment_weight = assessment["weight"]

                    # Get the plugin function which will perform the assessment
                    # and the respective parameters
                    assess_fun = assess_functions[assessment["name"]]
                    assess_params = assessment["params"]

                    # Get the student's repository local path
                    repo_local_path = student_git.repos[rule["repo"]]

                    # Perform assessment and obtain the assessment's grade
                    # between 0 and 1
                    assess_grade = assess_fun(repo_local_path, **assess_params)

                    # Update the grade for the current rule
                    rule_grade += assessment_weight * assess_grade

            # Update the grade for the current student
            student_grade += rule_weight * rule_grade

        print(f"Student {student_git.sid} grade is {student_grade}")
