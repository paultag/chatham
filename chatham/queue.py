# Copyright (c) 2012 Paul Tagliamonte <paultag@debian.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import datetime as dt
from monomoy.core import db
from fishhook import Hook


class ChathamQueue(Hook):
    def __init__(self):
        self._db = db
        self._build_types = db.build_types.find({
            "active": True
        })

    def enqueue(self, package_id, user_id):
        package = self._db.packages.find_one({"_id": package_id})
        if package is None:
            return  # XXX: Throw an exception

        user = self._db.users.find_one({"_id": user_id})
        if user is None:
            return  # XXX: Throw an exception, again.

        for build_type in self._build_types:
            build = build_type['_id']
            # XXX: Verify fitness somewhere.
            job_id = db.jobs.insert({
                "package": package['_id'],
                "user": user['_id'],
                "type": build,
                "builder": None,
                "queued_at": dt.datetime.now()
            }, safe=True)

            self.fire("chatham-queue-new-job", {
                "job_id": job_id,
                "user": user,
                "package": package,
                "type": build
            })

            yield job_id
