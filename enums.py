from enum import Enum


class JourneyCost(Enum):
    ZERO = 1
    CHEAP = 2
    AFFORDABLE = 3
    EXPENSIVE = 4
    UNKNOWN = 5

    def __repr__(self):
        return 'JourneyCost.{}'.format(self.name)

    def __gt__(self, other):
        if isinstance(other, JourneyCost):
            return self.value > other.value
        else:
            return NotImplemented


class DirectionMode(Enum):
    WALKING = 1
    DRIVING = 2
    BICYCLING = 3
    TRANSIT = 4

    def __repr__(self):
        return 'DirectionMode.{}'.format(self.name)


class Walking(Enum):
    SHORT = 1
    MEDIUM = 2
    LONG = 3

    def __repr__(self):
        return 'Walking.{}'.format(self.name)

    @staticmethod
    def cost():
        return JourneyCost.ZERO


class Driving(Enum):
    SHORT = 1
    MEDIUM = 2
    LONG = 3

    def __repr__(self):
        return 'Driving.{}'.format(self.name)

    @staticmethod
    def cost():
        return JourneyCost.AFFORDABLE


class Bicycling(Enum):
    SHORT = 1
    MEDIUM = 2
    LONG = 3

    def __repr__(self):
        return 'Bicycling.{}'.format(self.name)

    @staticmethod
    def cost():
        return JourneyCost.ZERO


class Transit(Enum):
    SHORT = 1
    MEDIUM = 2
    LONG = 3

    def __repr__(self):
        return 'Transit.{}'.format(self.name)

    @staticmethod
    def cost():
        return JourneyCost.ZERO


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
            'RAIL': JourneyCost.AFFORDABLE,
            'METRO_RAIL': JourneyCost.AFFORDABLE,
            'SUBWAY': JourneyCost.AFFORDABLE,
            'TRAM': JourneyCost.AFFORDABLE,
            'MONORAIL': JourneyCost.AFFORDABLE,
            'HEAVY_RAIL': JourneyCost.AFFORDABLE,
            'COMMUTER_TRAIN': JourneyCost.AFFORDABLE,
            'HIGH_SPEED_TRAIN': JourneyCost.AFFORDABLE,
            'BUS': JourneyCost.CHEAP,
            'INTERCITY_BUS': JourneyCost.AFFORDABLE,
            'TROLLEYBUS': JourneyCost.AFFORDABLE,
            'SHARE_TAXI': JourneyCost.AFFORDABLE,
            'FERRY': JourneyCost.AFFORDABLE,
            'CABLE_CAR': JourneyCost.AFFORDABLE,
            'GONDOLA_LIFT': JourneyCost.AFFORDABLE,
            'FUNICULAR': JourneyCost.AFFORDABLE,
            'OTHER': JourneyCost.AFFORDABLE,
        }

        return _cost_lookup[self.name]


class LegDuration(Enum):
    SHORT = 1
    MEDIUM = 2
    LONG = 3

    def __repr__(self):
        return 'LegDuration.{}'.format(self.name)


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

