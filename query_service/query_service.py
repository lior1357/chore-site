from collections import namedtuple
from typing import Type, Dict, List, Any, Iterable
from flask import jsonify, Response, abort
from dbsetup.models import Person, Chore
from repository import Repository
from .chore_availability import ChoreAvailability
import globals


class QueryService(object):

    # query methods
    @staticmethod
    def get_from_table(model: Type, **conditions: Dict) -> Response:
        query_results = Repository.read_from_table(model=model, **conditions)
        return jsonify(QueryService.serialize(query_results))

    @staticmethod
    def _get_from_table_serialized(model: Type, **conditions: Dict) -> List[Dict]:
        query_results = Repository.read_from_table(model=model, **conditions)
        return QueryService.serialize(query_results)

    @staticmethod
    def get_from_table_as_objects(model: Type, **conditions) -> List[Any]:
        query_results = Repository.read_from_table(model=model, **conditions)
        return [element for element in query_results]

    @staticmethod
    def get_chores_and_people_available_for_each(**conditions: Dict) -> Response:
        all_chores = QueryService.get_from_table_as_objects(Chore, **conditions)
        all_chores_with_people = QueryService.serialize(all_chores)

        for index, chore in enumerate(all_chores):
            all_chores_with_people[index]['people_available'] = QueryService.get_people_available_for_chore(chore)
            all_chores_with_people[index]['current_person'] = QueryService._get_from_table_serialized(Person, **{'id': chore.person_id})
        return jsonify(all_chores_with_people)

    @staticmethod
    def get_people_available_for_chore(chore: Chore) -> List[Dict]:
        people_available_for_chore = []
        service_status = ChoreAvailability.get_service_status_relevant_for_chore(chore)
        all_people = QueryService.get_from_table_as_objects(Person, **{'service_status': service_status})

        for person in all_people:
            if ChoreAvailability.is_person_available_for_chore(chore=chore, person=person) is True:
                people_available_for_chore.append(person)

        return QueryService.serialize(people_available_for_chore)

    @staticmethod
    def get_person_last_chore_by_chore_type(person: Person, chore_type=None) -> List[Dict]:
        conditions = {'person_id': person.personal_number}

        if chore_type is not None:
            conditions['chore_type'] = chore_type

        query_results = Repository.read_from_table(model=Chore, order_by=Chore.start_date, **conditions)[0]
        return QueryService.serialize(query_results)

    @staticmethod
    def get_person_last_chore(person: Person, chore: Chore):
        conditions = {'person_id': person.personal_number}
        query_results = Repository.read_from_table(model=Chore, order_by=Chore.start_date, **conditions)[0]
        return QueryService.serialize(query_results)

    # insertion method
    @staticmethod
    def insert_to_table(model: Type, entity_dict: Dict) -> bool:
        model_instance = model(**entity_dict)
        insertion_succeeded = Repository.insert_to_table(model_instance)

        return insertion_succeeded

    # deletion method
    @staticmethod
    def delete_one_from_table(model: Type, entity_dict: Dict):
        Repository.delete_from_table(model=model, one_row=True, **entity_dict)

    @staticmethod
    def delete_from_table(model: Type, condition_dict: Dict):
        Repository.delete_from_table(model=model, **condition_dict)

    # update method
    @staticmethod
    def update_table(model: Type, old_values: Dict, new_values: Dict):
        Repository.update_table_row(model, old_values, new_values)

    @staticmethod
    def serialize(query_results: Iterable) -> List[Dict]:
        return [element.to_dict() for element in query_results]