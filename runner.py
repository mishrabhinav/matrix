import logging
import pickle
import time
from datetime import datetime
from fim import apriori
from os import environ as env
from pprint import pformat

from pymodm import connect
from pymodm.errors import DoesNotExist

from core import listify, enumerize, DEFAULT_SETTINGS
from models import *


def _process_recommendations(recommendation, settings):
    forecasts = [forecast.data for forecast in recommendation.forecast]
    return enumerize(recommendation.selected.data['legs'][0], forecasts, settings)


def _generate_rules_for_user(recs, settings):
    tracts = []
    for rec in recs:
        if rec.selected and rec.forecast:
            tracts.append(_process_recommendations(rec, settings))

    if not tracts:
        return

    return [listify(rule) for rule in apriori(tracts, supp=-1)]


def _read_existing_rules():
    for rules in Rules.objects.all():
        mock_rules = pickle.loads(rules.rules)
        filtered_rules = [(rule, freq) for rule, freq in mock_rules if len(rule) >= 2]

        formatted_rules = pformat(filtered_rules)
        logging.info(
            'Reading {} rules for user <{}>, created at {}\n{}'.format(len(filtered_rules), rules.user,
                                                                       rules.created_on, formatted_rules))


def _generate_rules():
    gen_rules = []
    for user in User.objects.all():
        logging.info('Generating rules for user <{}>'.format(user.username))
        recommendations = Recommendations.objects.raw({'user': user.username})

        try:
            settings = Settings.objects.get({'username': user.username})
        except DoesNotExist:
            logging.warn('No settings found for <{}>, using default settings'.format(user.username))
            settings = DEFAULT_SETTINGS

        user_rules = _generate_rules_for_user(recommendations, settings)
        if user_rules:
            gen_rules.append(
                Rules(user=user.username, rules=pickle.dumps(user_rules), created_on=datetime.utcnow()))
        else:
            logging.warning('Not enough history for user <{}>'.format(user.username))

    # if gen_rules:
    #     Rules.objects.bulk_create(gen_rules)


def main():
    logging.Formatter.converter = time.gmtime
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)

    logging.info('Connecting to MongoDB')
    connect(env['MONGODB_URI'], alias="recommend-ahp")
    logging.info('Connected to MongoDB')

    _generate_rules()
    _read_existing_rules()


if __name__ == '__main__':
    main()
