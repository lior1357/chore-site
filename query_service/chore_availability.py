from typing import Dict
from dbsetup.models import Chore, Person
import globals


class ChoreAvailability(object):
    @staticmethod
    def is_person_available_for_chore(chore: Chore, person: Person) -> bool:
        if ChoreAvailability._has_person_exceeded_chore_amount(person, chore) is True:
            return False

        if ChoreAvailability._is_person_available_from_restraints_or_chores(chore, person) is False :
            return False

        return True

    @staticmethod
    def _has_person_exceeded_chore_amount(person: Person, chore: Chore) -> bool:
        person_chores = ChoreAvailability.get_person_chores_by_type(person)

        if chore.chore_type == 'hagnash':
            if person_chores['hagnash'] > 0:
                return True

        if chore.chore_type == 'ktzinto':
            if person_chores['ktzinto'] > 11:
                return True

        return False

    @staticmethod
    def _is_person_available_from_restraints_or_chores(chore: Chore, person: Person):
        chore_date_range = globals.DateRange(start=chore.start_date, end=chore.end_date)

        for restraint in person.restraints:
            restraint_date_range = globals.DateRange(start=restraint.start_date, end=restraint.end_date)
            if ChoreAvailability.if_date_ranges_overlap(chore_date_range, restraint_date_range) is True:
                return False

        for c in person.chores:
            c_date_range = globals.DateRange(start=c.start_date, end=c.end_date)

            if ChoreAvailability.if_date_ranges_overlap(chore_date_range, c_date_range) is True:
                return False

        return True

    @staticmethod
    def get_service_status_relevant_for_chore(chore: Chore):
        service_status = 'keva'

        if chore.chore_type in globals.chore_keys['hova']:
            service_status = 'hova'

        return service_status

    @staticmethod
    def if_date_ranges_overlap(r1: globals.DateRange, r2: globals.DateRange) -> bool:
        latest_start = max(r1.start, r2.start)
        earliest_end = min(r1.end, r2.end)
        delta = (earliest_end - latest_start).days

        return delta >= 0

    @staticmethod
    def initialize_chore_dict(person: Person):
        chore_dict = {}
        service_status = person.service_status

        for value in globals.chore_keys[service_status]:
            chore_dict[value] = 0

        return chore_dict

    @staticmethod
    def get_person_chores_by_type(person: Person) -> Dict:
        chore_dict = ChoreAvailability.initialize_chore_dict(person)

        for chore in person.chores:
            print(chore_dict)
            chore_dict[chore.chore_type] += 1

        return chore_dict

    @staticmethod
    def get_person_chores_ordered_by_type(person: Person) -> Dict:
        chore_dict = ChoreAvailability.initialize_chore_dict(person)

        for chore in person.chores:
            chore_dict[chore.chore_type] += 1

        return chore_dict
