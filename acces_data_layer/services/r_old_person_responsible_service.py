# This file contains the operations CRUD for the table `r_old_person_responsible`.
from typing import Optional, Type, List, Any
from sqlalchemy.orm import Session
from acces_data_layer.models.models import RelOldPersonResponsible
from acces_data_layer.services import engine


def insert(old_person_responsible_data: Any) -> None:
    """
    Inserts a new old person responsible into the database.

    Args:
      old_person_responsible_data: The old person responsible to insert.

    Returns:
      None.
    """
    with Session(engine) as session:
        old_person_responsible = RelOldPersonResponsible(**old_person_responsible_data)
        session.add(old_person_responsible)
        session.commit()


def select_all() -> List[dict]:
    """
    Returns all the old person responsible from the database.

    Returns:
      A list of old person responsible.
    """
    with Session(engine) as session:
        old_person_responsible = session.query(RelOldPersonResponsible).all()
        old_person_responsible_dict = [old_person_responsible.to_dict() for old_person_responsible in old_person_responsible]

    return old_person_responsible_dict


def update(old_person_responsible_data: Any) -> None:
    """
    Updates the old person responsible with the given ID in the database.
    """
    with Session(engine) as session:
        old_person_resp_current_state = RelOldPersonResponsible(**old_person_responsible_data.get('current_state'))
        old_person_resp_next_state = RelOldPersonResponsible(**old_person_responsible_data.get('next_state'))
        old_person_responsible = session.get(
            RelOldPersonResponsible, (
                old_person_resp_current_state.id_old_person,
                old_person_resp_current_state.id_responsible_person
            )
        )
        old_person_responsible.id_old_person = old_person_resp_next_state.id_old_person
        old_person_responsible.id_responsible_person = old_person_resp_next_state.id_responsible_person
        session.commit()


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
