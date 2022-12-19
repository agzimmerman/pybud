from enum import Enum
from datetime import date
from dataclasses import dataclass


@dataclass
class UncertainAmount:
    minimum: float = None
    maximum: float = None


class RecurrenceUnit(Enum):
    DAYS = 1
    WEEKS = 2
    MONTHS = 3
    YEARS = 4


@dataclass
class Recurrence:
    period: int
    unit: RecurrenceUnit
    start_date: date = None
    end_date: date = None
    handoff_id: int = None


@dataclass
class Transaction:
    label: str
    expected_amount: float
    minimum_amount: float = None
    maximum_amount: float = None
    transaction_date: date = None
    recurrence_start_date: date = None
    recurrence_end_date: date = None
    recurrence_unit: RecurrenceUnit = None
    recurrence_period: int = None
    recurrence_handoff_id: int = None
