from datetime import date, datetime, tzinfo
from typing import cast

from dateutil import parser


def interpret_datetime(obj: date | datetime | str, tzi: tzinfo | None) -> datetime:

    dt: datetime

    if isinstance(obj, date):
        dt = datetime.combine(cast(date, obj), datetime.min.time())
    elif isinstance(obj, datetime):
        dt = cast(datetime, obj)
    elif isinstance(obj, str):
        dt = parser.parse(cast(str, obj))
    else:
        raise SyntaxError(f"Unable to parse date/time given by '{obj}'")

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tzi)

    return dt
