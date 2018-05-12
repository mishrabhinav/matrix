import logging
import random

from .profile import Profile


class TypeA(Profile):
    def __init__(self, attributes):
        super().__init__(attributes)

    def go(self):
        prev_counter = self.counter.copy()

        [from_loc, to_loc] = random.sample(self.known_locations.keys(), 2)
        retrieve_resp = self._api_retrieve(self.known_locations[from_loc], self.known_locations[to_loc])

        rec_id = retrieve_resp['recommendation_id']
        loc_key = '{}{}'.format(from_loc, to_loc) if from_loc < to_loc else '{}{}'.format(to_loc, from_loc)

        directions = list(filter(lambda x: x['_mode'] in self.negative_mode, retrieve_resp['directions']))

        if directions:
            preferred = []
            for pref in self.preferred_mode[loc_key]:
                for dirn in directions:
                    if dirn['_mode'] == pref:
                        preferred.append(dirn)
                if preferred:
                    break

            if not preferred:
                preferred = directions

            preferred = list(filter(lambda x: x.get('_cost', 0.0) < self.max_spend, preferred))

            if self.shortest:
                preferred = sorted(preferred, key=lambda x: x['legs'][0]['duration']['value'])

            if self.fastest:
                preferred = sorted(preferred, key=lambda x: x['legs'][0]['distance']['value'])

            select_id = preferred[0]['_id']
            self._api_select(select_id, rec_id)

        logging.info('GO for {} from {} to {}'.format(self.name, from_loc, to_loc))

        return self.counter - prev_counter
