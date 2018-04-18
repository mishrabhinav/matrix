import json
from pprint import pprint

from enums import *
from arm import stats

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


def _norm_walking(steps):
    result = []
    distance = 0
    duration = 0

    for step in steps:
        distance += step['distance']['value']
        duration += step['duration']['value']

    if 0 < distance < 1000 or duration < 600:
        result.append(Walking.SHORT)
    elif 1000 <= distance < 2500 or 600 <= duration < 1200:
        result.append(Walking.MEDIUM)
    elif 2500 <= distance or 1200 <= duration:
        result.append(Walking.LONG)

    return result, duration


def _norm_bicycling(steps):
    result = []
    distance = 0
    duration = 0

    for step in steps:
        distance += step['distance']['value']
        duration += step['duration']['value']

    if 0 < distance < 2000 or 0 < duration < 600:
        result.append(Bicycling.SHORT)
    elif 2000 <= distance < 4000 or 600 <= duration < 1200:
        result.append(Bicycling.MEDIUM)
    elif 4000 <= distance or 1200 <= duration:
        result.append(Bicycling.LONG)

    return result, duration


def _norm_transit(steps):
    result = []
    distance = 0
    duration = 0

    for step in steps:
        distance += step['distance']['value']
        duration += step['duration']['value']
        result.append(TransitVehicle[step['transit_details']['line']['vehicle']['type']])

    if 0 < distance < 3000 or 0 < duration < 600:
        result.append(Transit.SHORT)
    elif 3000 <= distance < 6000 or 600 <= duration < 1200:
        result.append(Transit.MEDIUM)
    elif 6000 <= distance and 1200 <= duration:
        result.append(Transit.LONG)

    return result, duration


def _norm_driving(steps):
    result = []
    distance = 0
    duration = 0

    for step in steps:
        distance += step['distance']['value']
        duration += step['duration']['value']

    if 0 < distance < 3000 or 0 < duration < 600:
        result.append(Driving.SHORT)
    elif 3000 <= distance < 6000 or 600 <= duration < 1200:
        result.append(Driving.MEDIUM)
    elif 6000 <= distance or 1200 <= duration:
        result.append(Driving.LONG)

    return result, duration


_NORM_STEP_LOOKUP = {
    'WALKING': _norm_walking,
    'BICYCLING': _norm_bicycling,
    'TRANSIT': _norm_transit,
    'DRIVING': _norm_driving
}


def _norm_direction(direction):
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
        summary, mode_duration = _NORM_STEP_LOOKUP[mode](steps)
        travel_modes.extend(summary)
        duration += mode_duration

    cost = max([mode.cost() for mode in travel_modes], default=Cost.ZERO)
    travel_modes.append(cost)

    if duration < 900:
        travel_modes.append(Duration.SHORT)
    elif duration < 1500:
        travel_modes.append(Duration.MEDIUM)
    else:
        travel_modes.append(Duration.LONG)

    return travel_modes


def _norm_forecast(forecast, dest=False):
    icon = _FORECAST_LOOKUP[forecast['currently']['icon']]

    return EndForecast(icon) if dest else StartForecast(icon)


def enumerize(directions, forecasts):
    # TODO: Add Time enum
    transaction = _norm_direction(directions)
    transaction.append(_norm_forecast(forecasts[0]))
    transaction.append(_norm_forecast(forecasts[1], dest=True))

    return transaction


def listify(item):
    enums, count = item
    return list(enums), count
