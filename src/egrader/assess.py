"""Assessment functions."""

from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List, MutableSet, Sequence

from .cli_lib import check_empty_args
from .paths import (
    check_required_fp_exists,
    get_assessed_students_fp,
    get_student_repos_fp,
    get_valid_students_git_fp,
)
from .plugin import (
    get_short_plugin_desc,
    load_inter_repo_plugin_functions,
    load_repo_plugin_functions,
)
from .types import AssessedRepo, AssessedStudent, Assessment
from .yaml import load_yaml, save_yaml


def assess(assess_fp: Path, args: Namespace, extra_args: Sequence[str]) -> None:
    """Perform student assessment."""
    # extra_args should be empty
    check_empty_args(extra_args)

    # Check if assessment folder exists, and if not, quit
    check_required_fp_exists(assess_fp)

    # Determine rules file path
    rules_fp: Path = Path(args.rules_file)

    # Check if rules file exists, and if not, quit
    check_required_fp_exists(rules_fp)

    # Determine file path for valid students Git URL and repos yaml file
    students_git_fp: Path = get_valid_students_git_fp(assess_fp)

    # Check if valid students Git URL yaml file exists, and if not, quit
    check_required_fp_exists(students_git_fp)

    # Load rules
    rules = load_yaml(rules_fp)

    # Load student list and their URLs
    students_git = load_yaml(students_git_fp, safe=False)

    # Obtained all the repository assessments defined by the rules
    required_assessments: MutableSet[str] = {
        assess_rule["name"]
        for rule in rules
        if "assessments" in rule
        for assess_rule in rule["assessments"]
    }

    # Load required assessment plugins as specified by the rules
    assess_functions: Dict[str, Any] = load_repo_plugin_functions(required_assessments)

    # Initialize student grades list
    assessed_students: List[AssessedStudent] = []

    # Initialize dictionary of assessed repositories by name, which will be
    # required later for inter-repository assessments
    repos_by_name: Dict[str, List[AssessedRepo]] = {rule["repo"]: [] for rule in rules}

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
                # Get the student's repository local path
                assessed_repo.local_path = student_git.repos[rule["repo"]]

                # Append repository being assessed to dictionary of repositories
                # by name (will be required later for inter-repository assessments)
                repos_by_name[rule["repo"]].append(assessed_repo)

                # Loop through the assessments to be made for the current rule's
                # repository, if any
                if "assessments" in rule:
                    for assess_rule in rule["assessments"]:
                        # Get the plugin function which will perform the assessment
                        # and the respective parameters
                        assess_fun = assess_functions[assess_rule["name"]]
                        assess_params = assess_rule.get("params", {})

                        # Perform assessment and obtain the assessment's grade
                        # between 0 and 1
                        assess_grade = assess_fun(
                            student_git, assessed_repo.local_path, **assess_params
                        )

                        # Create assessment object
                        assessment = Assessment(
                            assess_rule["name"],
                            get_short_plugin_desc(assess_fun),
                            assess_params,
                            assess_rule["weight"],
                            assess_grade,
                        )

                        # Add it to the repository currently being assessed
                        assessed_repo.add_assessment(assessment)

            # Add assessed repo to student being assessed
            assessed_student.add_assessed_repo(assessed_repo)

        # Add assessed student to list of assessed students
        assessed_students.append(assessed_student)

    # Obtained all the repository assessments defined by the rules
    required_inter_assessments: MutableSet[str] = {
        inter_assess_rule["name"]
        for rule in rules
        if "inter_assessments" in rule
        for inter_assess_rule in rule["inter_assessments"]
    }

    # Load required inter-assessment plugins as specified by the rules
    inter_assess_functions: Dict[str, Any] = load_inter_repo_plugin_functions(
        required_inter_assessments
    )

    # Apply intra-repository assessments
    for rule in rules:
        if "inter_assessments" in rule:
            for inter_assess_rule in rule["inter_assessments"]:
                repos_with_name: List[AssessedRepo] = repos_by_name[rule["repo"]]

                inter_assess_fun = inter_assess_functions[inter_assess_rule["name"]]
                inter_assess_params = inter_assess_rule.get("params", {})

                # Perform inter-repo assessment and obtain the assessment's
                # grade between 0 and 1
                inter_assess_grades = inter_assess_fun(
                    [sr.local_path for sr in repos_with_name], **inter_assess_params
                )

                # Create assessments (one per repos with the current name)
                assessments = [
                    Assessment(
                        inter_assess_rule["name"],
                        get_short_plugin_desc(inter_assess_fun),
                        inter_assess_params,
                        inter_assess_rule["weight"],
                        iag,
                    )
                    for iag in inter_assess_grades
                ]

                # Add assessments to each repo with the current name
                for ar, a in zip(repos_with_name, assessments, strict=True):
                    ar.add_inter_assessment(a)

    # Determine file path where to save assessment information
    assessed_students_fp: Path = get_assessed_students_fp(assess_fp)

    # Save list of assessed students to yaml file
    save_yaml(assessed_students_fp, assessed_students)

    # Number of assessments performed
    n_assessments = sum([s.assessment_count for s in assessed_students])

    # Provide feedback to the user
    print(f"- Absolute assessment path: {assess_fp.absolute()}.")
    print(f"- Fetched student repository information from {students_git_fp}")
    print(
        f"- Performed {n_assessments} assessments on {len(assessed_students)} "
        f"student repositories at {get_student_repos_fp(assess_fp)}."
    )
    print(f"- Updated {assessed_students_fp}.")
