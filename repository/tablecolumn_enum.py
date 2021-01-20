from enum import Enum


class PersonModelEnum(Enum):
    ID = 'id'
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    LAST_HAGNASH = 'last_hagnash'
    NUM_OF_HAGNASH = 'num_of_hagnash'


class RestraintModelEnum(Enum):
    ID = 'id'
    START_DATE = 'start_date'
    END_DATE = 'end_date'
    PERSON_ID = 'person_id'


class ChoreModelEnum(Enum):
    ID = 'id'
    START_DATE = 'start_date'
    END_DATE = 'end_date'
    CHORE_TYPE = 'chore_type'
    PERSON_SENT = 'person_sent'
    PERSON_REZERVA = 'person_rezerva'
