
# owner:
# abilities: []
# ping:

import datetime as dt
from monomoy.core import db


class ChathamBuilder(Hook):
    def __init__(self, bid):
        cache = db.builders.find_one({"_id": bid})
        if cache is None:
            return  # Raise exception.
        self._cache = cache

    def ping(self):
        self._cache['ping'] = dt.datetime.now()
        self.update()

    def update(self):
        db.builders.update({"_id": self._cache['_id']},
                           self._cache, safe=True)

    def get_abilities(self):
        pass
