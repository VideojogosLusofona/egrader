"""Functions used by the command-line interface."""

from typing import Final, Sequence

OPT_E_SHORT: Final[str] = "e"
OPT_E_LONG: Final[str] = "existing"
OPT_E_STOP: Final[str] = "stop"
OPT_E_UPDT: Final[str] = "update"
OPT_E_OVWR: Final[str] = "overwrite"


class CLIArgError(Exception):
    """Error raised when command-line arguments are invalid."""


def check_empty_args(args: Sequence[str]) -> None:
    """Check that argument list is empty, otherwise raise error."""
    if len(args) > 0:
        raise CLIArgError(None, f"Invalid arguments: {', '.join(args)}")
