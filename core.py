import os
from math import ceil
from datetime import datetime

if os.environ.get('MATRIX'):
    from matrix.enums import *
else:
    from enums import *

DEFAULT_SETTINGS = {
    'distance': [3000, 6000],
    'duration': [1200, 1800],
    'WALKING': {
        'show': True,
        'distance': [1000, 2500],
        'duration': [600, 1200]
    },
    'BICYCLING': {
        'show': True,
        'distance': [2000, 4000],
        'duration': [600, 1200]
    },
    'DRIVING': {
        'show': True,
        'distance': [3000, 6000],
        'duration': [600, 1200]
    },
    'TRANSIT': {
        'show': True,
        'distance': [3000, 6000],
        'duration': [600, 1200]
    }
}

_ENUM_LOOKUP = {
    'WALKING': Walking,
    'BICYCLING': Bicycling,
    'TRANSIT': Transit,
    'DRIVING': Driving
}

_FORECAST_LOOKUP = {
    'clear-day': 1,
    'clear-night': 2,
    'rain': 3,
    'snow': 4,
    'sleet': 5,
    'wind': 6,
    'fog': 7,
    'cloudy': 8,
    'partly-cloudy-day': 9,
    'partly-cloudy-night': 10
}


def _norm_steps(steps, settings, mode):
    result = []
    transit_vehicles = []
    tot_distance = 0
    tot_duration = 0

    distance = settings['distance']
    duration = settings['duration']
    enum = _ENUM_LOOKUP[mode]

    for step in steps:
        tot_distance += step['distance']['value']
        tot_duration += step['duration']['value']

        if mode.upper() == 'TRANSIT':
            transit_vehicles.append(TransitVehicle[step['transit_details']['line']['vehicle']['type']])

    result.extend(set(transit_vehicles))

    if 0 < tot_distance < distance[0] or tot_duration < duration[0]:
        result.append(enum.SHORT)
    elif distance[0] <= tot_distance < distance[1] or duration[0] <= tot_duration < duration[1]:
        result.append(enum.MEDIUM)
    elif distance[1] <= tot_distance or duration[1] <= tot_duration:
        result.append(enum.LONG)

    return result, tot_duration


def _norm_direction(direction, settings):
    duration = 0
    travel_modes = []
    grouped_steps = {
        'WALKING': [],
        'BICYCLING': [],
        'TRANSIT': [],
        'DRIVING': []
    }

    steps = direction['steps']
    for step in steps:
        grouped_steps[step['travel_mode']].append(step)

    for mode, steps in grouped_steps.items():
        if not steps:
            continue

        summary, mode_duration = _norm_steps(steps, settings[mode], mode)
        travel_modes.extend(summary)
        duration += mode_duration

    cost = max([mode.cost() for mode in travel_modes], default=Cost.ZERO)
    travel_modes.append(cost)

    if duration < settings['duration'][0]:
        travel_modes.append(Duration.SHORT)
    elif duration < settings['duration'][1]:
        travel_modes.append(Duration.MEDIUM)
    else:
        travel_modes.append(Duration.LONG)

    return travel_modes


def _norm_forecast(forecast, dest=False):
    icon = _FORECAST_LOOKUP[forecast['currently']['icon']]

    return EndForecast(icon) if dest else StartForecast(icon)


def _norm_journey_time(created_on: datetime):
    hour = created_on.hour

    if 0 <= hour < 4:
        return Time.LATE_NIGHT
    elif 4 <= hour < 7:
        return Time.EARLY_MORNING
    elif 7 <= hour < 12:
        return Time.MORNING
    elif 12 <= hour < 17:
        return Time.AFTERNOON
    elif 17 <= hour < 21:
        return Time.EVENING
    elif 21 <= hour:
        return Time.NIGHT


def enumerize(directions, forecasts, created_on, settings=DEFAULT_SETTINGS):
    """Deprecated. Use enum_repr instead.
    """
    return enum_repr(directions, forecasts, created_on, settings)


def enum_repr(directions, forecasts, created_on, settings=DEFAULT_SETTINGS):
    # TODO: Add Time enum
    transaction = _norm_direction(directions, settings)
    transaction.append(_norm_forecast(forecasts[0]))
    transaction.append(_norm_forecast(forecasts[1], dest=True))
    transaction.append(_norm_journey_time(created_on))

    return transaction


def listify(item):
    enums, count = item
    return list(enums), count


def _retrieve_criterion_token(criterion, tract):
    for t in tract:
        if isinstance(t, criterion):
            return t


class Matrix:
    def __init__(self, rules, metadata):
        self.rules = {str(key): value for key, value in rules}
        self.metadata = metadata

    def __len__(self):
        return len(self.rules)

    def compare(self, criterion, alt_1, alt_2):
        if not self.rules:
            return 1

        tok_1 = _retrieve_criterion_token(criterion, alt_1)
        tok_2 = _retrieve_criterion_token(criterion, alt_2)

        num_tok_1 = self.rules.get(str([tok_1]), 1)
        num_tok_2 = self.rules.get(str([tok_2]), 1)

        diff_toks = (num_tok_1 - num_tok_2) / self.metadata['total_trips']

        if num_tok_1 == num_tok_2:
            return 1
        elif num_tok_1 > num_tok_2:
            return ceil(diff_toks * 10)
        else:
            return 1 / ceil(abs(diff_toks) * 10)
