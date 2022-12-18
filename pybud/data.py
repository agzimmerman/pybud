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
    uncertain_amount: UncertainAmount = None
    transaction_date: date = None
    recurrence: Recurrence = None

    def __init__(
            self,
            label: str,
            expected_amount: float,
            transaction_date: date,
            # Uncertain amount
            minimum_amount:  float = None,
            maximum_amount: float = None,
            # Recurrence
            recurrence_start_date: date = None,
            recurrence_end_date: date = None,
            recurrence_unit: RecurrenceUnit = None,
            recurrence_period: int = None,
            recurrence_handoff_id: int = None
    ):
        self.label = label
        self.expected_amount = expected_amount

        if minimum_amount is not None or maximum_amount is not None:
            self.uncertain_amount = UncertainAmount(minimum_amount, maximum_amount)

        self.date = transaction_date

        if recurrence_period is not None and recurrence_unit is not None:
            self.recurrence = Recurrence(
                period=recurrence_period,
                unit=recurrence_unit,
                start_date=recurrence_start_date,
                end_date=recurrence_end_date,
                handoff_id=recurrence_handoff_id
            )
