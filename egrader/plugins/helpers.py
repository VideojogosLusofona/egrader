"""Helper functions for the various plug-ins."""

from datetime import date, datetime, tzinfo
from typing import cast

from dateutil import parser


def interpret_datetime(obj: date | datetime | str, tzi: tzinfo | None) -> datetime:
    """Try to convert an object into a [datetime][datetime.datetime] instance."""
    dt: datetime

    if isinstance(obj, str):
        dt = parser.parse(cast(str, obj))
    elif isinstance(obj, datetime):
        dt = cast(datetime, obj)
    elif isinstance(obj, date):
        dt = datetime.combine(cast(date, obj), datetime.min.time())
    else:
        raise SyntaxError(f"Unable to parse date/time given by {obj!r}")

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tzi)

    return dt
