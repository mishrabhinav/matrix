from fim import apriori, fpgrowth
from pprint import pprint


def stats(tracts, pre=None, post=None, algorithm='apriori', args={}):
    if pre and callable(pre):
        tracts = map(pre, tracts)

    tracts = list(tracts)
    pprint(tracts, width=120)

    if algorithm not in globals():
        raise ValueError('{} algorithm not available'.format(algorithm))

    rules = globals()[algorithm](tracts, **args)

    if post and callable(post):
        rules = map(post, rules)

    return rules


def get_confidence():
    # TODO: Implement
    pass
