# This file contains the operations CRUD for the table `responsible_person`.
from typing import Optional, Type, List
from sqlalchemy.orm import Session
from acces_data_layer.models.models import ResponsiblePerson
from acces_data_layer.services import engine


def insert(resp_person: ResponsiblePerson):
    """
    Inserts a new responsible person into the database.

    Args:
      resp_person: The responsible person to insert.

    Returns:
      None.
    """
    with Session(engine) as session:
        session.add(resp_person)
        session.commit()


def select() -> List[ResponsiblePerson]:
    """
    Returns all the responsible persons from the database.

    Returns:
      A list of responsible persons.
    """
    with Session(engine) as session:
        resp_person = session.query(ResponsiblePerson).all()
        return resp_person


def select_by_id(id_resp_person: int) -> Optional[Type[ResponsiblePerson]]:
    """
    Returns the responsible person with the given ID.

    Args:
      id_resp_person: The ID of the responsible person to return.

    Returns:
      The responsible person with the given ID, or `None` if no responsible person with that ID is found.
    """
    with Session(engine) as session:
        resp_person = session.get(ResponsiblePerson, id_resp_person)
        return resp_person


def update(resp_person: ResponsiblePerson):
    """
    Updates a responsible person in the database.

    Args:
      resp_person: The responsible person to update.

    Returns:
      None.
    """
    with Session(engine) as session:
        current_person = session.get(ResponsiblePerson, resp_person.id_responsible_person)
        current_person.responsible_person_name = resp_person.responsible_person_name
        session.commit()


def delete(id_resp_person: int):
    """
    Deletes the responsible person with the given ID from the database.

    Args:
      id_resp_person: The ID of the responsible person to delete.

    Returns:
      None.
    """
    with Session(engine) as session:
        resp_person = session.get(ResponsiblePerson, id_resp_person)
        session.delete(resp_person)
        session.commit()
