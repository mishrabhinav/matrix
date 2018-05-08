from abc import ABC, abstractmethod
from collections import Counter
from os import environ as env
import logging

import requests


class ProfileException(Exception):
    pass


class Profile(ABC):
    def __init__(self, attributes):
        name = attributes['name']
        self.access_token = env['{}_ACCESS'.format(name)]
        self.attributes = attributes
        self.counter = Counter(gmaps_directions=0, ds_forecasts=0, api_retrieve=0, api_select=0)

        if not self._check_auth():
            raise ProfileException('Check Access Token for {}'.format(name))

    def _check_auth(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
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
        logging.info('<{}> {}'.format(self.attributes['name'], self.counter))

    @abstractmethod
    def go(self):
        # Request a journey and select an alternative based on attributes
        pass
