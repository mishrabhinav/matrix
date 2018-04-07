import json
from pprint import pprint

from enums import *
from fim import stats

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
    distance = 0
    duration = 0

    for step in steps:
        distance += step['distance']['value']
        duration += step['duration']['value']

    if distance == 0 or duration == 0:
        return []
    elif distance < 1000 or duration < 600:
        return [Walking.SHORT]
    elif distance < 2500 or duration < 1200:
        return [Walking.MEDIUM]
    else:
        return [Walking.LONG]


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

    return result


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

    return result


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

    return result


_NORM_STEP_LOOKUP = {
    'WALKING': _norm_walking,
    'BICYCLING': _norm_bicycling,
    'TRANSIT': _norm_transit,
    'DRIVING': _norm_driving
}


def _norm_direction(direction):
    grouped_steps = {
        'WALKING': [],
        'BICYCLING': [],
        'TRANSIT': [],
        'DRIVING': []
    }

    steps = direction['steps']
    for step in steps:
        grouped_steps[step['travel_mode']].append(step)

    travel_modes = []
    for mode, steps in grouped_steps.items():
        travel_modes.extend(_NORM_STEP_LOOKUP[mode](steps))

    cost = max([mode.cost() for mode in travel_modes], default=JourneyCost.ZERO)
    travel_modes.append(cost)

    return travel_modes


def _norm_forecast(forecast, dest=False):
    icon = _FORECAST_LOOKUP[forecast['currently']['icon']]

    return EndForecast(icon) if dest else StartForecast(icon)


def enumerize(item):
    transaction = _norm_direction(item['directions'])
    transaction.append(_norm_forecast(item['forecast'][0]))
    transaction.append(_norm_forecast(item['forecast'][1], dest=True))

    return transaction


def listify(item):
    enums, count = item
    return list(enums), count


if __name__ == '__main__':
    tracts = []
    with open('data.json') as fp:
        tracts = json.load(fp)

    rules = list(stats(tracts, pre=enumerize, post=listify, algorithm='fpgrowth', args={'supp': 3}))

    pprint(rules)
    print('------------------------------')
    print('Number of rules generated: {}'.format(len(rules)))
