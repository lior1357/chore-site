from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

Base = declarative_base()


class Person(Base, SerializerMixin):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    personal_number = Column(String(7), index=True, unique=True, nullable=False)
    first_name = Column(String(64), index=False, nullable=False)
    last_name = Column(String(64), index=False, nullable=False)
    points = Column(Integer, index=False, default=0)
    service_status = Column(Integer, index=False, nullable=False)
    chores = relationship("Chore", primaryjoin="or_("
                                               "Person.id==Chore.person_id,"
                                               "Person.id==Chore.person_rezerva_id"
                                               ")", viewonly=True)
    restraints = relationship("Restraint")

    def __repr__(self):
        return {'first_name': self.first_name, 'last_name': self.last_name, 'personal_number': self.personal_number}


class Restraint(Base, SerializerMixin):
    __tablename__ = 'restraints'

    id = Column(Integer, primary_key=True, autoincrement=True, key='id')
    start_date = Column(DateTime, index=False, nullable=False, key='start_date')
    end_date = Column(DateTime, index=False, nullable=False, key='end_date')
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False,  key='person_id')
    __table_args__ = (UniqueConstraint('start_date', 'end_date', 'person_id',  name='restraints_uc'),)

    def __repr__(self):
        return 'restraint {}: by {} {} {}'.format(self.id, self.person_id, self.start_date, self.end_date)

    def __eq__(self, other):
        self.id = other.id
        self.start_date = other.start_date
        self.end_date = other.end_date
        self.person_id = other.person_id


class Chore(Base, SerializerMixin):
    __tablename__ = 'chore'

    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime, index=False, nullable=False)
    end_date = Column(DateTime, index=False, nullable=False)
    chore_type = Column(String(10), index=False, nullable=False)
    points = Column(Integer, index=False, nullable=True, key='points')
    person_id = Column(String(7), ForeignKey('person.id'), key='person_id')
    person_rezerva_id = Column(Integer, ForeignKey('person.id'), key='person_rezerva')

    def __repr__(self):
        return 'chore: {} from {} to {}'.format(self.chore_type, self.start_date, self.end_date)

    def __eq__(self, other):
        self.id = other.id
        self.start_date = other.start_date()
        self.end_date = other.end_date
        self.chore_type = other.chore_type


class Couples(Base, SerializerMixin):
    __tablename__ = 'couples'

    id = Column(Integer, primary_key=True)
    person1 = Column(Person, index=False, nullable=False)
    person2 = Column(Person, index=False, nullable=False)