from typing import List

from sqlalchemy import select

from acces_data_layer.models.models import Medicine
from acces_data_layer import db_session


def insert(medicine: Medicine) -> None:
    """
    Inserts a new medicine into the database.

    Args:
        medicine: The Medicine object to insert

    Returns:
        None

    Description:
        Opens a SQLAlchemy db_session. Adds the Medicine object.
        Commits change to persist in the database.
    """
    db_session.add(medicine)
    db_session.commit()


def select_all() -> List[Medicine]:
    """
    Gets all medicines from the database.

    Args:
        None

    Returns:
        medicines: List of Medicine objects

    Description:
        Opens a SQLAlchemy db_session. Queries for all Medicine rows.
        Returns them in a list.
    """
    medicines = db_session.scalars(
        select(Medicine)
    ).all()

    return medicines


def select_by_id(id_medicine: int) -> Medicine:
    """
    Gets a medicine by ID.

    Args:
        id_medicine: The ID of the medicine

    Returns:
        medicine: The Medicine object found
    Description:
    Opens a SQLAlchemy db_session. Queries for Medicines Medicine if found, otherwise returns None.
"""
    medicine = db_session.get(Medicine, id_medicine)

    return medicine


def select_by_name(medicine_name: str) -> int:
    """
    Gets a medicine by name.

    Args:
        medicine_name: The medicine name

    Returns:
        medicine: The Medicine object not found
    Description:
    Opens a SQLAlchemy db_session. Queries for Medicines if found, otherwise returns None.
"""
    result = db_session.scalars(
         select(Medicine).filter_by(medicine_name=medicine_name).limit(1)
    ).first()

    return result.id_medicine if result else None


def update(medicine: Medicine):
    """
    Updates an existing medicine.

    Args:
        medicine: The Medicine object to update

    Returns:
        None

    Description:
        Opens SQLAlchemy db_session. Gets existing Medicine by ID.
        Sets its fields to the passed Medicine object. Commits changes.
    """
    db_session.merge(medicine)
    db_session.commit()


def delete(id_medicine: int):
    """
    Deletes a medicine by ID.

    Args:
        id_medicine: The ID of the medicine to delete

    Returns:
        None

    Description:
        Opens SQLAlchemy db_session. Gets existing Medicine by ID.
        Deletes from db_session. Commits changes.
    """
    medicine = db_session.get(Medicine, id_medicine)
    db_session.delete(medicine)
    db_session.commit()
