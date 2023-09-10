# This file contains the operations CRUD for the table `old_person`.
from typing import Optional, Type, List
from sqlalchemy.orm import Session, joinedload
from acces_data_layer.models.models import OldPerson
from acces_data_layer.services import engine


def insert(old_person: OldPerson):
    """
    Inserts a new old person into the database.

    Args:
      old_person: The old person to insert.

    Returns:
      None.
    """
    with Session(engine) as session:
        session.add(old_person)
        session.commit()


def select_all() -> List[Type[OldPerson]]:
    """
    Returns all the old persons from the database.

    Returns:
      A list of old persons.
    """
    with Session(engine) as session:
        old_persons = session.query(OldPerson).options(
            joinedload(OldPerson.responsible_persons),
            joinedload(OldPerson.activities),
            joinedload(OldPerson.medicines),
            joinedload(OldPerson.feedings),
            joinedload(OldPerson.exercises)
        ).all()
        return old_persons


def select_by_id(id_old_person: int) -> Optional[Type[OldPerson]]:
    """
    Returns the old person with the given ID.

    Args:
      id_old_person: The ID of the old person to return.

    Returns:
      The old person with the given ID, or `None` if no old person with that ID is found.
    """
    with Session(engine) as session:
        old_person = session.query(OldPerson).options(
            joinedload(OldPerson.responsible_persons),
            joinedload(OldPerson.activities),
            joinedload(OldPerson.medicines),
            joinedload(OldPerson.feedings),
            joinedload(OldPerson.exercises)
        ).get(id_old_person)
        return old_person


def update(old_person: OldPerson):
    """
    Updates an old person in the database.

    Args:
      old_person: The old person to update.

    Returns:
      None.
    """
    with Session(engine) as session:
        current_person = session.get(OldPerson, old_person.id_old_person)
        current_person.old_person_name = old_person.old_person_name
        session.commit()


def delete(id_old_person: int):
    """
    Deletes the old person with the given ID from the database.

    Args:
      id_old_person: The ID of the old person to delete.

    Returns:
      None.
    """
    with Session(engine) as session:
        old_person = session.get(OldPerson, id_old_person)
        session.delete(old_person)
        session.commit()
