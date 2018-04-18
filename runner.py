import logging
import pickle
import time
from datetime import datetime
from os import environ as env

from fim import apriori
from pymodm import connect

from core import listify, enumerize
from models import *


def _process_recommendations(recommendation):
    forecasts = [forecast.data for forecast in recommendation.forecast]
    return enumerize(recommendation.selected.data['legs'][0], forecasts)


def _generate_rules_for_user(recs):
    tracts = []
    for rec in recs:
        if rec.selected and rec.forecast:
            tracts.append(_process_recommendations(rec))

    if not tracts:
        return

    return [listify(rule) for rule in apriori(tracts, supp=100)]


def _read_existing_rules():
    for rules in Rules.objects.all():
        mock_rules = pickle.loads(rules.rules)
        print(mock_rules, rules.created_on)


def _generate_rules():
    gen_rules = []
    for user in User.objects.all():
        logging.info('Generating rules for user <{}>'.format(user.username))
        recommendations = Recommendations.objects.raw({'user': user.username})

        user_rules = _generate_rules_for_user(recommendations)
        if user_rules:
            gen_rules.append(Rules(user=user.username, rules=pickle.dumps(user_rules), created_on=datetime.utcnow()))
        else:
            logging.warning('Not enough history for user <{}>'.format(user.username))

    if gen_rules:
        Rules.objects.bulk_create(gen_rules)


def main():
    logging.Formatter.converter = time.gmtime
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)

    logging.info('Connecting to MongoDB')
    connect("mongodb://{}:{}/{}".format(env['MONGO_IP'], env['MONGO_PORT'], env['MONGO_DB']), alias="recommend-ahp")
    logging.info('Connected to MongoDB')

    _generate_rules()


if __name__ == '__main__':
    main()
