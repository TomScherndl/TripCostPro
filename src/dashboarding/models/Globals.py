import pandas as pd
from dashboarding.models.Commodity import Commodity

TIME_ZONE = "Europe/Brussels"
FREQUENCY = "h"
DATE_FORMAT = "YYYY-MM-DD HH:mm"
MIN_TIME = pd.Timestamp("20240101", tz=TIME_ZONE)
MAX_TIME = pd.Timestamp("20260101", tz=TIME_ZONE)
FUEL_KWH_PER_L = {
    Commodity.DIESEL: 9.7,
    Commodity.EUROSUPER: 8.9,
    Commodity.NORMAL: 8.9,
    Commodity.SUPER_PLUS: 8.9,
}
