# This file contains the operations CRUD for the table `responsible_person`.
from typing import List

from sqlalchemy import select

from acces_data_layer import db_session
from acces_data_layer.models.models import ResponsiblePerson


def insert(resp_person: ResponsiblePerson):
    """
    Inserts a new responsible person into the database.

    Args:
      resp_person: The responsible person to insert.

    Returns:
      None.
    """
    db_session.add(resp_person)
    db_session.commit()


def select_all() -> List[ResponsiblePerson]:
    """
    Returns all the responsible persons from the database.

    Returns:
      A list of responsible persons.
    """
    resp_persons = db_session.scalars(
        select(ResponsiblePerson)
    ).all()

    return resp_persons


def select_by_id(id_resp_person: int) -> ResponsiblePerson:
    """
    Returns the responsible person with the given ID.

    Args:
      id_resp_person: The ID of the responsible person to return.

    Returns:
      The responsible person with the given ID, or `None` if no responsible person with that ID is found.
    """
    resp_person = db_session.get(ResponsiblePerson, id_resp_person)
    return resp_person


def update(resp_person: ResponsiblePerson):
    """
    Updates a responsible person in the database.

    Args:
      resp_person: The responsible person to update.

    Returns:
      None.
    """
    db_session.merge(resp_person)
    db_session.commit()


def delete(id_resp_person: int):
    """
    Deletes the responsible person with the given ID from the database.

    Args:
      id_resp_person: The ID of the responsible person to delete.

    Returns:
      None.
    """

    resp_person = db_session.get(ResponsiblePerson, id_resp_person)
    db_session.delete(resp_person)
    db_session.commit()
