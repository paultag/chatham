
from fishhook import Hook
from monomoy.core import db
from chatham.queue import ChathamQueue

class PackageAccepted(Hook):
    def fire(self, caller, event, obj):
        user = obj['user']
        package = obj['package']
        changes = db.packages.find_one({"_id": package})
        build_for = changes['changes']['Distribution']
