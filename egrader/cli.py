import argparse
from pathlib import Path

def main():
    """
    This function is called when the script is invoked with the `egrader` command.
    """

    # Create an argument parser
    parser = argparse.ArgumentParser(description='Exercise Grader.',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Specify arguments to parse
    parser.add_argument('-r', '--repos', type=str, metavar='<REPOS FILE>',
                        help='Student repositories file in TSV format',
                        default='repos.tsv')
    parser.add_argument('-a', '--assessment', type=str, metavar='<RULES FILE>',
                        help='Assessment rules in YAML format',
                        default='rules.yml')
    parser.add_argument('-o', '--output-folder', type=str, metavar='<OUTPUT FOLDER>',
                        help='Output folder',
                        default=Path('out'))

    # Parse and validate command line arguments
    args = parser.parse_args()

    # Show args
    print("-s", args.repos)
    print("-a", args.assessment)
    print("-o", args.output_folder)
