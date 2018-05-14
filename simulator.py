import argparse
import logging
import time
import json
import glob
from collections import Counter

from profiles import TypeA


def _parse_args():
    parser = argparse.ArgumentParser(description='Simulate user profiles on the Recommend API')
    parser.add_argument('-w', '--wait-interval',
                        type=int,
                        default=120,
                        help='wait time between two go actions')

    return parser.parse_args()


def _get_profile_class(prof_type, attributes):
    if prof_type == 'A':
        return TypeA(attributes)

    return


def _main():
    counter = Counter(gmaps_directions=0, ds_forecasts=0, api_retrieve=0, api_select=0)
    args = _parse_args()

    files = glob.glob('data/*.json')
    user_profiles = []
    for prof_file in files:
        with open(prof_file) as prof_json:
            attributes = json.loads(prof_json.read())
            user_profiles.append(_get_profile_class(attributes['type'], attributes))

    while True:
        for prof in user_profiles:
            prof_counter_update = prof.go()
            counter = prof_counter_update + counter

            prof.log_stats()

        logging.info('GLOBAL {}'.format(counter))
        time.sleep(args.wait_interval)


if __name__ == '__main__':
    logging.Formatter.converter = time.gmtime
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)

    _main()
