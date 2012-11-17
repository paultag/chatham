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

from chatham.errors import ChathamError
from monomoy.core import db
from fishhook import Hook


class ChathamBuilderNotFound(ChathamError):
    pass


class Builder(Hook):
    def __init__(self, name):
        self._db = db
        obj = db.builders.find_one({"_id": name})
        if obj is None:
            raise ChathamBuilderNotFound(name)

        self._obj = obj

    def ping(self):
        self._obj['ping'] = dt.datetime.now()
        self.save()

    def disable(self):
        self._obj['active'] = False
        self.save()

    def enable(self):
        self._obj['active'] = True
        self.save()

    def purge(self):
        pass

    def get_owner(self):
        pass

    def get_authorized_users(self):
        pass

    def save(self):
        obj = self._obj
        self._db.builders.update({"_id": obj['_id']},
                                 obj,
                                 safe=True)
