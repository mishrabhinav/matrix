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


def enumerize(directions, forecasts, settings=DEFAULT_SETTINGS):
    # TODO: Add Time enum
    transaction = _norm_direction(directions, settings)
    transaction.append(_norm_forecast(forecasts[0]))
    transaction.append(_norm_forecast(forecasts[1], dest=True))

    return transaction


def listify(item):
    enums, count = item
    return list(enums), count
