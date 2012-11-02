
import datetime as dt
from monomoy.core import db
from fishhook import Hook

class ChathamQueue(Hook):
    def __init__(self):
        self._db = db

    def enqueue(self, package_id, user_id):
        package = self._db.packages.find_one({"_id": package_id})
        if package is None:
            return  # XXX: Throw an exception

        user = self._db.users.find_one({"_id": user_id})
        if user is None:
            return  # XXX: Throw an exception, again.

        job_id = db.jobs.insert({
            "package": package['_id'],
            "user": user['_id'],
            "builds": [],
            "entered_queue": dt.datetime.now()
        }, safe=True)

        return job_id
