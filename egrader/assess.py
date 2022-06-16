from importlib.metadata import EntryPoints, entry_points
from inspect import getdoc
from pathlib import Path
from typing import List, MutableSet

from .common import (
    AssessedRepo,
    AssessedStudent,
    Assessment,
    check_required_fp_exists,
    get_assessed_students_fp,
    get_output_fp,
    get_valid_students_git_fp,
)
from .yaml import load_yaml, save_yaml


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
    assess_plugins: EntryPoints = entry_points(group="egrader.assess")

    # Create a set of all required assessments
    required_assessments: MutableSet[str] = set()
    for rule in rules:
        for assess_rule in rule["assessments"]:
            required_assessments.add(assess_rule["name"])

    # Load required assessment plugins as specified by the rules
    assess_functions = {}
    for ap in assess_plugins:
        if ap.name in required_assessments:
            assess_functions[ap.name] = ap.load()
        else:
            # TODO Raise error
            pass

    # Initialize student grades list
    assessed_students: List[AssessedStudent] = []

    # Apply rules and assessments to each student
    for student_git in students_git:

        # Create instance of current student's assessment
        assessed_student: AssessedStudent = AssessedStudent(student_git.sid)

        # Loop through rules
        for rule in rules:

            # Create an instance of the repository being assessed
            assessed_repo: AssessedRepo = AssessedRepo(rule["repo"], rule["weight"])

            # If student has the repository specified in the current rule, apply
            # the specified assessments
            if rule["repo"] in student_git.repos:

                # Loop through the assessments to be made for the current rule's
                # repository
                for assess_rule in rule["assessments"]:

                    # Get the plugin function which will perform the assessment
                    # and the respective parameters
                    assess_fun = assess_functions[assess_rule["name"]]
                    assess_params = assess_rule["params"]

                    # Get the student's repository local path
                    repo_local_path = student_git.repos[rule["repo"]]

                    # Perform assessment and obtain the assessment's grade
                    # between 0 and 1
                    assess_grade = assess_fun(repo_local_path, **assess_params)

                    # Create assessment object
                    assessment = Assessment(
                        assess_rule["name"],
                        get_desc(assess_fun),
                        assess_rule["weight"],
                        assess_grade,
                    )

                    # Add it to the repository currently being assessed
                    assessed_repo.add_assessment(assessment)

            # Add assessed repo to student being assessed
            assessed_student.add_assessed_repo(assessed_repo)

        # Add assessed student to list of assessed students
        assessed_students.append(assessed_student)

    # Save list of assessed students to yaml file
    save_yaml(get_assessed_students_fp(output_fp), assessed_students)


def get_desc(func):
    """Get a short description of the assessment function."""

    desc = getdoc(func)

    if desc is not None and len(desc) > 0:
        desc = desc.split("\n")[0]
    else:
        desc = "Unavailable"

    return desc