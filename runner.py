import logging
import pickle
import time
from datetime import datetime
from fim import apriori
from os import environ as env

from pymodm import connect
from pymodm.errors import DoesNotExist

from core import listify, enumerize, DEFAULT_SETTINGS, Matrix
from models import *


def _process_recommendations(recommendation, settings):
    forecasts = [forecast.data for forecast in recommendation.forecast]
    return enumerize(recommendation.selected.data['legs'][0], forecasts, settings)


def _generate_rules_for_user(recs, settings):
    tracts = []
    for rec in recs:
        if rec.selected and rec.forecast:
            tracts.append(_process_recommendations(rec, settings))

    metadata = {
        'total_trips': len(tracts)
    }

    if not tracts:
        return None, metadata

    return [listify(rule) for rule in apriori(tracts, supp=-1)], metadata


def _read_existing_rules():
    for rules in Rules.objects.all():
        rule_matrix: Matrix = pickle.loads(rules.rules)

        logging.info(
            'Read {} rules for user <{}>, created at {}\n'.format(len(rule_matrix), rules.user,
                                                                  rules.created_on))


def _generate_rules():
    gen_rules = []
    for user in Settings.objects.all():
        logging.info('Generating rules for user <{}>'.format(user.username))
        recommendations = Recommendations.objects.raw({'user': user.username})

        settings = user.data

        if not settings:
            logging.warning('No settings found for <{}>, using default settings'.format(user.username))
            settings = DEFAULT_SETTINGS

        user_rules, metadata = _generate_rules_for_user(recommendations, settings)
        if user_rules:
            gen_rules.append(
                Rules(user=user.username, rules=pickle.dumps(Matrix(user_rules, metadata)),
                      created_on=datetime.utcnow()))
        else:
            logging.warning('Not enough history for user <{}>'.format(user.username))

    if gen_rules:
        Rules.objects.bulk_create(gen_rules)


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
