
from monomoy.core import db
from fishhook import Hook

class ChathamQueue(Hook):
    def __init__(self):
        self._db = db
