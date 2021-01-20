from collections import namedtuple
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker
from flask import current_app

engine = None
Session = None
DateRange = None
chore_keys = None


def initialize(db_uri):
    global engine
    global Session
    global DateRange
    global chore_keys

    engine = create_engine(db_uri, echo=True, poolclass=pool.NullPool, connect_args={"check_same_thread": False})
    Session = sessionmaker()
    Session.configure(bind=engine)
    DateRange = namedtuple('Range', ['start', 'end'])
    chore_keys = {'keva': ('hagnash', 'ktzinto', 'keva'), 'hova': ('hova',)}
