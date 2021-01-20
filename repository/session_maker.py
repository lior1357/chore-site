from sqlite3 import IntegrityError
from flask import abort
import globals


class SessionMaker(object):

    def __init__(self, func):
        self.function = func

    def __call__(self, *args, **kwargs):
        session = globals.Session()
        res = self.function(session=session, *args, **kwargs)
        session.close()
        return res

