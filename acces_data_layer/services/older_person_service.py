# This file contains the operations CRUD for the table `older_person`.
from typing import List

from sqlalchemy import select

from acces_data_layer import db_session
from acces_data_layer.models.models import OlderPerson


def insert(older_person: OlderPerson) -> None:
    """
    Inserts a new old person into the database.

    Args:
      older_person: The old person to insert.

    Returns:
      None.
    """
    db_session.add(older_person)
    db_session.commit()


def select_all() -> List[OlderPerson]:
    """
    Returns all the old persons from the database.

    Returns:
      A list of old persons.
    """
    older_persons = db_session.scalars(
        select(OlderPerson)
    ).all()

    return older_persons


def select_by_id(id_older_person: int) -> OlderPerson:
    """
    Returns the old person with the given ID.

    Args:
      id_older_person: The ID of the old person to return.

    Returns:
      The old person with the given ID, or `None` if no old person with that ID is found.
    """
    older_person = db_session.get(OlderPerson, id_older_person)

    return older_person


def update(older_person: OlderPerson):
    """
    Updates an old person in the database.

    Args:
      older_person: The old person to update.

    Returns:
      None.
    """
    db_session.merge(older_person)
    db_session.commit()


def delete(id_older_person: int):
    """
    Deletes the old person with the given ID from the database.

    Args:
      id_older_person: The ID of the old person to delete.

    Returns:
      None.
    """
    older_person = db_session.get(OlderPerson, id_older_person)
    db_session.delete(older_person)
    db_session.commit()
