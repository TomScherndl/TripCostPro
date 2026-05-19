from enum import StrEnum
from dashboarding.models.Commodity import Commodity



class CarColumns(StrEnum):
    NAME = "Name"
    COMMODITY = "Commodity"
    CONSUMPTION = "Consumption"
    UNIT = "kWh" if Commodity.ELETRICITY else "liter"
    TRIP_COST = "Trip cost (EUR)"
    IN_BUDGET = "In budget"