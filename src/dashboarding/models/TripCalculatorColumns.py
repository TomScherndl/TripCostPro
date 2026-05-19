from enum import StrEnum
from dashboarding.models.CarColumns import CarColumns
from dashboarding.models.Commodity import Commodity


class TripCalculatorColumns(StrEnum):
    NAME = CarColumns.NAME.value
    COMMODITY = CarColumns.COMMODITY.value
    CONSUMPTION = CarColumns.CONSUMPTION.value
    UNIT = "kWh/100km" if CarColumns.COMMODITY.value == Commodity.ELETRICITY else "l/100km"
    TRIP_COST = "Trip cost (EUR)"
    IN_BUDGET = "In budget"