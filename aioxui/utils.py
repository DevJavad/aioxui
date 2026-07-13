from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from hijridate import Gregorian
import jdatetime

from .enums import Calendar, UnitType


class Storage:
    BYTE = 1
    KB = 1024
    MB = KB * 1024
    GB = MB * 1024
    TB = GB * 1024
    PB = TB * 1024

    _UNITS = {
        UnitType.BYTE: BYTE,
        UnitType.KB: KB,
        UnitType.MB: MB,
        UnitType.GB: GB,
        UnitType.TB: TB,
        UnitType.PB: PB,
    }

    @classmethod
    def from_unit(cls, value: int | float, unit: UnitType) -> int:
        """
        Convert a size to bytes.

        Example:
            Storage.from_unit(10, Unit.GB)
            -> 10737418240
        """
        return int(value * cls._UNITS[unit])

    @classmethod
    def to_unit(cls, value: int, unit: UnitType) -> float:
        """
        Convert bytes to selected unit.

        Example:
            Storage.to_unit(10737418240, Unit.GB)
            -> 10
        """
        return value / cls._UNITS[unit]

    @classmethod
    def format(cls, value: int, precision: int = 2) -> str:
        """
        Human readable size.

        Example:
            Storage.format(10737418240)
            -> 10 GB
        """

        units = [
            (UnitType.PB, cls.PB),
            (UnitType.TB, cls.TB),
            (UnitType.GB, cls.GB),
            (UnitType.MB, cls.MB),
            (UnitType.KB, cls.KB),
            (UnitType.BYTE, cls.BYTE),
        ]

        for unit, size in units:
            if value >= size:
                return f"{round(value / size, precision)} {unit.upper()}"

        return f"{value} {UnitType.BYTE}"


class DateTime:
    @staticmethod
    def now() -> int:
        """Current Unix timestamp in milliseconds."""
        return int(datetime.now(timezone.utc).timestamp() * 1000)

    @staticmethod
    def after(**kwargs) -> int:
        """
        Create a future Unix timestamp.

        Example:
            DateTime.after(days=30)
            DateTime.after(months=6, hours=5)
        """
        return int(
            (datetime.now(timezone.utc) + relativedelta(**kwargs)).timestamp() * 1000
        )

    @staticmethod
    def to_datetime(timestamp: int) -> datetime:
        """Convert Unix timestamp (ms) to UTC datetime."""
        return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)

    @classmethod
    def remaining(
        cls,
        timestamp: int,
        from_datetime: datetime | None = None,
    ) -> relativedelta:
        """Remaining time until timestamp."""
        if from_datetime is None:
            from_datetime = datetime.now(timezone.utc)

        return relativedelta(cls.to_datetime(timestamp), from_datetime)

    @classmethod
    def to_calendar(
        cls,
        timestamp: int,
        calendar: Calendar = Calendar.GREGORIAN,
        format: str | None = None,
    ):
        """
        Convert timestamp to selected calendar.

        Example:

            DateTime.to_calendar(
                ts,
                Calendar.JALALI,
                "%Y/%m/%d %H:%M"
            )

        """

        dt = cls.to_datetime(timestamp)

        match calendar:

            case Calendar.GREGORIAN:
                result = dt

            case Calendar.JALALI:
                result = jdatetime.datetime.fromgregorian(datetime=dt)

            case Calendar.HIJRI:
                result = Gregorian(dt.year, dt.month, dt.day).to_hijri()

            case _:
                raise ValueError(f"Unsupported calendar: {calendar}")

        if format:
            return result.strftime(format)

        return result