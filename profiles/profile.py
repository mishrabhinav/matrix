import logging
from abc import ABC, abstractmethod
from collections import Counter
from os import environ as env

import requests


class ProfileException(Exception):
    pass


class Profile(ABC):
    def __init__(self, attributes):
        # Attributes
        self.name: str = attributes['name']
        self.known_locations: dict = attributes['knownLocations']
        self.preference: list = attributes['orderOfPreference']
        self.negative_mode: list = attributes['negative']
        self.preferred_mode: dict = attributes['preferredModes']
        self.max_spend: float = attributes['maxSpend']
        self.shortest: bool = attributes['shortest']
        self.fastest: bool = attributes['fastest']

        self.access_token = 'Bearer {}'.format(env['{}_ACCESS'.format(self.name)])
        self.counter = Counter(gmaps_directions=0, ds_forecasts=0, api_retrieve=0, api_select=0)

        if not self._check_auth():
            raise ProfileException('Check Access Token for {}'.format(self.name))
        else:
            logging.info('Authenticated {}'.format(self.name))

    def _check_auth(self):
        headers = {
            'Authorization': self.access_token
        }

        r = requests.get('{}/api'.format(env['API_URL']), headers=headers)

        if r.status_code == requests.codes.ok:
            return True
        elif r.status_code <= requests.codes.bad:
            print('Warning: Auth check for {} received non-200 code'.format(self.attributes['name']))
            return True
        else:
            return False

    def log_stats(self):
        logging.info('<{}> {}'.format(self.name, self.counter))

    def _api_retrieve(self, from_coord, to_coord):
        headers = {
            'Authorization': self.access_token
        }

        url = '{}/api/retrieve?from={},{}&to={},{}'.format(env['API_URL'], from_coord[0], from_coord[1], to_coord[0],
                                                           to_coord[1])

        r = requests.get(url, headers=headers)
        r.raise_for_status()

        self.counter['gmaps_directions'] += 4
        self.counter['ds_forecasts'] += 2
        self.counter['api_retrieve'] += 1

        return r.json()

    def _api_select(self, select, recommendation_id):
        headers = {
            'Authorization': self.access_token,
            'Content-Type': 'application/json'
        }

        url = '{}/api/select'.format(env['API_URL'])
        data = {
            'recommendation_id': recommendation_id,
            'select': select
        }

        r = requests.post(url, data=data, headers=headers)
        r.raise_for_status()

        self.counter['api_select'] += 1

    @abstractmethod
    def go(self):
        # Request a journey and select an alternative based on attributes
        pass
