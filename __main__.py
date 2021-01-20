import os
import threading
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort
from flask_cors import CORS, cross_origin
import datetime
from dbsetup import models
from query_service.query_service import QueryService
import globals
from dbsetup.models import Base

app = Flask(__name__, instance_relative_config=True)
CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)
CONFIG_OBJECT_STRING = 'config_file.Config'


def create_app(test_config=None):
    # create and configure the app
    load_config_tp_app()
    globals.initialize(db_uri=app.config['SQLALCHEMY_DATABASE_URI'])
    initialize_db()
    ensure_instance_folder_exists()

    @app.route('/read/people', methods=['GET'])
    @cross_origin()
    def get_all_from_person_table():
        return QueryService.get_from_table(models.Person)

    @app.route('/read/chore', methods=['GET'])
    @cross_origin()
    def get_all_from_chore_table():

        print('\n\n\n\n')
        print('calm down')
        return QueryService.get_chores_and_people_available_for_each()
        # return QueryService.get_from_table(models.Person, **{'id': 7})

    @app.route('/update/chore', methods=['GET', 'PUT'])
    @cross_origin()
    def get_chore_info():

        if request.method == 'GET':
            chore_id = request.args['id']
            conditions = {'id': chore_id}
            return QueryService.get_chores_and_people_available_for_each(**conditions)

        else:
            data = request.get_json()
            chore_id = data['id']
            conditions = {'id': chore_id}
            dates = get_dates_from_request(data)
            chore_type = data['choreType']
            person_sent = data['personIDSent']

            new_values = {'start_date': dates[0], 'end_date': dates[1], 'chore_type': chore_type, 'person_id': person_sent}
            QueryService.update_table(models.Chore, conditions, new_values)
            return {'value': True}

    @app.route('/test2', methods=['POST'])
    @cross_origin()
    def insert_chore():
        data = request.get_json()

        start_date = data['startDate']
        start_date = datetime.date(*(int(s) for s in start_date.split('-')))

        end_date = data['endDate']
        end_date = datetime.date(*(int(s) for s in end_date.split('-')))

        print(data)
        res = QueryService.insert_to_table(models.Chore, {'start_date': start_date, 'end_date': end_date,
                                                   'chore_type': data['choreType']})
        if res is False:
            abort(409)

        return {'value': res}

        # abort(409)  # raise database error id unique constraint fails

    @app.route('/insert/restraint', methods=['POST'])
    @cross_origin()
    def insert_restraint():
        data = request.get_json()
        dates = get_dates_from_request(data)
        res = QueryService.insert_to_table(models.Restraint, {'start_date': dates[0], 'end_date': dates[1], 'person_id': data['person']})
        if res is False:
            abort(409)

        return {'value': res}

    @app.route('/insert/person', methods=['POST'])
    @cross_origin()
    def insert_person():
        data = request.get_json()
        print(data)
        res = QueryService.insert_to_table(models.Person, {'first_name': data['firstname'], 'last_name': data['lastname'],
                                          'personal_number': data['personalNumber'], 'service_status': data['serviceStatus']})

        return {'value': res}

    @app.route('/')
    @cross_origin()
    def hello():
        print(f'{threading.current_thread()} desirable thread')
        #yes = QueryService.insert_to_table(models.Restraint, {'start_date': datetime.datetime(2014, 11, 10), 'end_date': datetime.datetime(2007, 10, 10), 'person_id': 1})
        #print(yes)
        print (type(QueryService.get_from_table(models.Person)))
        return QueryService.get_from_table(models.Person)
    return app


def initialize_db():
    db.init_app(app)
    with app.app_context():
        db.create_all()
    Base.metadata.create_all(globals.engine)


def load_config_tp_app(test_config=None):
    if test_config is None:
        app.config.from_object(CONFIG_OBJECT_STRING)
    else:
        app.config.from_mapping(test_config)


def ensure_instance_folder_exists():
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


def get_dates_from_request(data):
    start_date = data['startDate']
    start_date = datetime.date(*(int(s) for s in start_date.split('-')))

    end_date = data['endDate']
    end_date = datetime.date(*(int(s) for s in end_date.split('-')))

    return tuple([start_date, end_date])


if __name__ == '__main__':
    create_app().run()
