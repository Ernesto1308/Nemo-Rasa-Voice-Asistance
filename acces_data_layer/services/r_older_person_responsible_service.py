# This file contains the operations CRUD for the table `r_old_person_responsible`.
from typing import List

from sqlalchemy import select

from acces_data_layer.models.models import RelOlderPersonResponsible
from acces_data_layer import db_session


def insert(older_person_responsible: RelOlderPersonResponsible) -> None:
    """
    Inserts a new old person responsible into the database.

    Args:
      older_person_responsible: The old person responsible to insert.

    Returns:
      None.
    """
    db_session.add(older_person_responsible)
    db_session.commit()


def select_all() -> List[RelOlderPersonResponsible]:
    """
    Returns all the old person responsible from the database.

    Returns:
      A list of old person responsible.
    """

    older_person_responsible = db_session.scalars(
        select(RelOlderPersonResponsible)
    ).all()

    return older_person_responsible


def select_by_id(identifier: int) -> RelOlderPersonResponsible:
    """
    Args:
      identifier: The ID of the relation between old person responsible to return.

    Returns:
      The relation between old person responsible with the given ID from the database.
    """
    older_person_responsible = db_session.get(RelOlderPersonResponsible, identifier)

    return older_person_responsible


def update(older_person_responsible: RelOlderPersonResponsible) -> None:
    """
    Updates the old person responsible with the given ID in the database.
    """
    db_session.merge(older_person_responsible)
    db_session.commit()


def delete(identifier: int):
    """
    Deletes the old person responsible with the given ID from the database.

    Args:
      identifier: The ID of the relation to delete.

    Returns:
      None.
    """
    older_person_responsible = db_session.get(RelOlderPersonResponsible, identifier)
    db_session.delete(older_person_responsible)
    db_session.commit()
