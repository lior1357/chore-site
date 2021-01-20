from flask import abort
from sqlalchemy.exc import IntegrityError
from typing import Dict, Type
from sqlalchemy.orm import Query
import globals
from dbsetup.models import Base
from .session_maker import SessionMaker


class Repository(object):

    @staticmethod
    def _check_query_columns_valid(model: Type, keys: Dict):
        table_cols = model.__table__.c.keys()

        # the keys that were sent and are not in thr table
        wrong_keys = [a for a in keys.keys() if a not in table_cols]

        # the rest of the keys in the table other than the wrong ones
        right_keys = [k for k in keys.keys() if k not in wrong_keys]

        # the keys that were'nt sent but need to be sent
        required_keys = [elem for elem in table_cols if elem not in right_keys
                         and model.__table__.c[elem].nullable is False]

        # check if the query is fine or else raise exception
        if sorted(right_keys) != sorted(keys.keys()):
            raise Exception("The arguments you entered are incomplete or incorrect. The arguments {} do not exist."
                            " you need to add the following args: {}.     {}".format(wrong_keys, required_keys,
                                                                                     right_keys))

    @staticmethod
    @SessionMaker
    def delete_from_table(model: Type, one_row=False, session=None, **conditions):
        query = session.query(model).filter_by(**conditions)

        if query is not None:
            if one_row is True:
                query = query.first()

            for entity in query:
                session.delete(entity)

        session.commit()

    @staticmethod
    @SessionMaker
    def insert_to_table(inserted_value: Base, session=None):
        try:
            session.add(inserted_value)
            session.commit()
            return True

        except IntegrityError as e:
            print(str(e))
            abort(409)
            return False

    @staticmethod
    @SessionMaker
    def update_table_row(model: Base, old_values: Dict, new_values: Dict, session=None):
        query = session.query(model).filter_by(**old_values)
        query.update(new_values)
        session.commit()

    @staticmethod
    @SessionMaker
    def read_from_table(model: Type,  session=None, order_by=None, **conditions: Dict) -> Query:
        Repository._check_query_columns_valid(model=model, keys=conditions)

        if order_by is None:
            return session.query(model).filter_by(**conditions)
        else:
            return session.query(model).filter_by(**conditions).order_by(order_by.desc())







