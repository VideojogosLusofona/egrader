from typing import Sequence


class CLIArgError(Exception):
    """Error raised when command-line arguments are invalid."""


def check_empty_args(args: Sequence[str]) -> None:
    """Check that argument list is empty, otherwise raise error."""

    if len(args) > 0:
        raise CLIArgError(None, f"Invalid arguments: {', '.join(args)}")
