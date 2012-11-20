from debuild import app, API_BASE, serialize

from monomoy.core import db
from bson.objectid import ObjectId

from flask import render_template, abort


@app.route("%s/ping" % (API_BASE))
def ping():
    return serialize({
        "ping": True
    })
