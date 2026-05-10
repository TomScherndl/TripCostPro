from enum import StrEnum
from dashboarding.models.CarColumns import CarColumns


class TripCalculatorColumns(StrEnum):
    NAME = CarColumns.NAME.value
    COMMODITY = CarColumns.COMMODITY.value
    CONSUMPTION = CarColumns.CONSUMPTION.value
    TRIP_COST = "Trip cost (EUR)"
    IN_BUDGET = "In budget"