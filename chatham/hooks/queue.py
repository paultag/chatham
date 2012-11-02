
from fishhook import Hook
from monomoy.core import db
from chatham.queue import ChathamQueue

class PackageAccepted(Hook):
    def fire(self, caller, event, obj):
        user = obj['user']['_id']
        package = obj['package']
        changes = db.packages.find_one({"_id": package})
        q = ChathamQueue()
        job = q.enqueue(package, user)
        print "Job %s created." % (job)
