from enum import StrEnum


class Calendar(StrEnum):
    GREGORIAN = "gregorian"
    JALALI = "jalali"
    HIJRI = "hijri"


class UnitType(StrEnum):
    BYTE = "byte"
    KB = "kb"
    MB = "mb"
    GB = "gb"
    TB = "tb"
    PB = "pb"