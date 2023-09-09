# This file contains the operations CRUD for the table `r_old_person_responsible`.
from typing import Optional, Type, List
from sqlalchemy.orm import Session
from acces_data_layer.models.models import RelOldPersonResponsible
from acces_data_layer.services import engine


def insert(old_person_responsible: RelOldPersonResponsible):
    """
    Inserts a new old person responsible into the database.

    Args:
      old_person_responsible: The old person responsible to insert.

    Returns:
      None.
    """
    with Session(engine) as session:
        session.add(old_person_responsible)
        session.commit()


def select() -> List[RelOldPersonResponsible]:
    """
    Returns all the old person responsible from the database.

    Returns:
      A list of old person responsible.
    """
    with Session(engine) as session:
        old_person_responsible = session.query(RelOldPersonResponsible).all()

    return old_person_responsible


def delete(id_old_person: int, id_responsible_person: int):
    """
    Deletes the old person responsible with the given ID from the database.

    Args:
      id_old_person: The ID of the old person to delete.
      id_responsible_person: The ID of the person responsible to delete.

    Returns:
      None.
    """
    with Session(engine) as session:
        old_person_responsible = session.get(RelOldPersonResponsible, (id_old_person, id_responsible_person))
        session.delete(old_person_responsible)
        session.commit()
