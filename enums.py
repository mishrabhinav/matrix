from enum import Enum


class Time(Enum):
    EARLY_MORNING = 1  # 04:00 to 06:59
    MORNING = 2        # 7:00 to 11:59
    AFTERNOON = 3      # 12:00 to 16:59
    EVENING = 4        # 17:00 to 20:59
    NIGHT = 5          # 21:00 to 23:59
    LATE_NIGHT = 6     # 00:00 to 03:59

    def __repr__(self):
        return 'Time.{}'.format(self.name)


class Cost(Enum):
    ZERO = 1
    CHEAP = 2
    AFFORDABLE = 3
    EXPENSIVE = 4
    UNKNOWN = 5

    def __repr__(self):
        return 'Cost.{}'.format(self.name)

    def __gt__(self, other):
        if isinstance(other, Cost):
            return self.value > other.value
        else:
            return NotImplemented


class Mode(Enum):
    WALKING = 1
    DRIVING = 2
    BICYCLING = 3
    TRANSIT = 4

    def __repr__(self):
        return 'Mode.{}'.format(self.name)


class Walking(Enum):
    SHORT = 1
    MEDIUM = 2
    LONG = 3

    def __repr__(self):
        return 'Walking.{}'.format(self.name)

    @staticmethod
    def cost():
        return Cost.ZERO


class Driving(Enum):
    SHORT = 1
    MEDIUM = 2
    LONG = 3

    def __repr__(self):
        return 'Driving.{}'.format(self.name)

    @staticmethod
    def cost():
        return Cost.AFFORDABLE


class Bicycling(Enum):
    SHORT = 1
    MEDIUM = 2
    LONG = 3

    def __repr__(self):
        return 'Bicycling.{}'.format(self.name)

    @staticmethod
    def cost():
        return Cost.ZERO


class Transit(Enum):
    SHORT = 1
    MEDIUM = 2
    LONG = 3

    def __repr__(self):
        return 'Transit.{}'.format(self.name)

    @staticmethod
    def cost():
        return Cost.ZERO


class TransitVehicle(Enum):
    RAIL = 1
    METRO_RAIL = 2
    SUBWAY = 3
    TRAM = 4
    MONORAIL = 5
    HEAVY_RAIL = 6
    COMMUTER_TRAIN = 7
    HIGH_SPEED_TRAIN = 8
    BUS = 9
    INTERCITY_BUS = 10
    TROLLEYBUS = 11
    SHARE_TAXI = 12
    FERRY = 13
    CABLE_CAR = 14
    GONDOLA_LIFT = 15
    FUNICULAR = 16
    OTHER = 17

    def __repr__(self):
        return 'TransitMode.{}'.format(self.name)

    def cost(self):
        _cost_lookup = {
            'RAIL': Cost.AFFORDABLE,
            'METRO_RAIL': Cost.AFFORDABLE,
            'SUBWAY': Cost.AFFORDABLE,
            'TRAM': Cost.AFFORDABLE,
            'MONORAIL': Cost.AFFORDABLE,
            'HEAVY_RAIL': Cost.AFFORDABLE,
            'COMMUTER_TRAIN': Cost.AFFORDABLE,
            'HIGH_SPEED_TRAIN': Cost.AFFORDABLE,
            'BUS': Cost.CHEAP,
            'INTERCITY_BUS': Cost.AFFORDABLE,
            'TROLLEYBUS': Cost.AFFORDABLE,
            'SHARE_TAXI': Cost.AFFORDABLE,
            'FERRY': Cost.AFFORDABLE,
            'CABLE_CAR': Cost.AFFORDABLE,
            'GONDOLA_LIFT': Cost.AFFORDABLE,
            'FUNICULAR': Cost.AFFORDABLE,
            'OTHER': Cost.AFFORDABLE,
        }

        return _cost_lookup[self.name]


class Duration(Enum):
    SHORT = 1
    MEDIUM = 2
    LONG = 3

    def __repr__(self):
        return 'Duration.{}'.format(self.name)


class StartForecast(Enum):
    CLEAR_DAY = 1
    CLEAR_NIGHT = 2
    RAIN = 3
    SNOW = 4
    SLEET = 5
    WIND = 6
    FOG = 7
    CLOUDY = 8
    PARTLY_CLOUDY_DAY = 9
    PARTLY_CLOUDY_NIGHT = 10

    def __repr__(self):
        return 'StartForecast.{}'.format(self.name)


class EndForecast(Enum):
    CLEAR_DAY = 1
    CLEAR_NIGHT = 2
    RAIN = 3
    SNOW = 4
    SLEET = 5
    WIND = 6
    FOG = 7
    CLOUDY = 8
    PARTLY_CLOUDY_DAY = 9
    PARTLY_CLOUDY_NIGHT = 10

    def __repr__(self):
        return 'EndForecast.{}'.format(self.name)

