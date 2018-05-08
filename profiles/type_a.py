from collections import Counter

from .profile import Profile


class TypeA(Profile):
    def __init__(self):
        super().__init__({'name': 'Phil'})

    def go(self):
        prev_counter = self.counter.copy()
        self.counter['api_retrieve'] += 1
        return self.counter - prev_counter
